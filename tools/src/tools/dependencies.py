# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    dependencies.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/03 11:13:24 by dfine             #+#    #+#              #
#    Updated: 2025/05/14 14:55:34 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from uuid import uuid4

import fitz
import jwt
import requests
from loguru import logger
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_MEDIA_TYPE
from pydantic import BaseModel
from tiktoken import encoding_for_model
from tqdm import tqdm

from tools.wrap_funcs import get_time_async, get_time_sync

from . import (
    ADMIN_PASSWORD,
    ADMIN_USER,
    DOC_SERV_JWT_SECRET,
    DOCUMENT_API,
    FILE_SERVER_PREFIX,
    GATEWAY,
    SERVER_PREFIX,
    STATIC_DIR,
)
from .definitions import (
    AssetInfo,
    AudioInfo,
    FeedbackType,
    FileListResponse,
    GameListResponse,
    GatewayResponse,
    ImageInfo,
    LlmSlideInfo,
    LlmSlideList,
    PptConvertResponse,
    PptInfo,
    PptResponseModel,
    PptSlideList,
    SlideInfo,
)
from .tag_agent import TagAgent


class PptParseRequest(BaseModel):
    ppt_file: str


@lru_cache
def login(
    user: str = ADMIN_USER, password: str = ADMIN_PASSWORD, gateway: str = GATEWAY
) -> str | None:
    payload = {"username": user, "password": password}
    response = requests.post(f"{gateway}/user/login", json=payload)
    if response.status_code != 200:
        return None
    response_json = GatewayResponse.model_validate(response.json())
    if response_json.code != 200:
        return None
    token = response_json.result
    return f"Bearer {token}" if token is not None else token


auth_token = login()


@lru_cache
def get_mcp_check_prompt() -> str:
    return """
# ESLint Syntax Requirements

After generating any TypeScript code, ensure it is fully compliant with ESLint rules.

The user will automatically validate your output using ESLint in MCP (Machine-Consumable Protocol) mode. This means your code must pass strict syntax and style checks.

If there are any linting or syntax issues, you must revise and regenerate the code until it passes ESLint without errors. Prioritize producing clean, correct, and standards-compliant TypeScript code in your first response whenever possible.

Do not ignore ESLint errors — your output will not be accepted unless it is valid TypeScript code with zero ESLint violations.
""".strip()


def encode_jwt(payload):
    return jwt.encode(payload, DOC_SERV_JWT_SECRET, algorithm="HS256")


def pdf2image(file_path: Path, out_path: Path) -> list[Path] | None:
    if (
        not file_path.exists()
        or not file_path.is_file()
        or file_path.suffix.lower() != ".pdf"
    ):
        logger.info(f"{file_path} is not a valid pdf file")
        return None
    if out_path.exists() and not out_path.is_dir():
        logger.info(f"{out_path} is not a valid directory")
        return None
    out_path.mkdir(parents=True, exist_ok=True)
    images_path: list[Path] = []
    with fitz.open(file_path) as pdf:
        for page_index in tqdm(range(len(pdf))):
            page = pdf[page_index]
            pix = page.get_pixmap()
            image_path = out_path / f"page_{page_index + 1}.png"
            pix.save(str(image_path))
            images_path.append(image_path)
    return images_path


# ppt to pdf
def doc_convert(
    file_path: Path,
    out_path: Path,
    output_filename: str = "output.pdf",
    output_type: str = "pdf",
) -> Path | None:
    if not file_path.exists() or not file_path.is_file():
        logger.info(f"{file_path} is not a valid file")
        return None
    if out_path.exists() and not out_path.is_dir():
        logger.info(f"{out_path} is not a valid directory")
        return None
    out_path.mkdir(parents=True, exist_ok=True)
    payload = {
        "async": False,
        "filetype": file_path.suffix.lstrip("."),
        "key": str(uuid4()),
        "outputtype": output_type,
        "url": SERVER_PREFIX + str(file_path),
    }
    token = encode_jwt({"payload": payload})
    logger.info(f"payload: \n {payload}")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    logger.info(DOCUMENT_API)
    res = requests.post(url=DOCUMENT_API, headers=headers, json=payload)
    logger.info(res.json)
    if res.status_code != 200:
        logger.info(
            f"failed to convert {file_path} to pdf: {res.status_code} {res.text}"
        )
        return None

    try:
        res_json: dict[str, str] = res.json()
        logger.info(res_json)
        pdffile = requests.get(res_json.get("fileUrl", ""))
        output = out_path / output_filename
        _ = open(output, "wb").write(pdffile.content)
        return out_path / output_filename
    except Exception as e:
        logger.error("conversion failed: error ", e)
        return None


def doc2img(file_address: str) -> PptConvertResponse | None:
    file_path = Path(file_address)
    out_path = file_path.parent / "convert"
    file_name = "output.pdf"

    pdf_path = doc_convert(file_path, out_path, file_name)
    if not pdf_path:
        logger.info("doc convert failed")
        return
    images_path = pdf2image(pdf_path, pdf_path.parent / "images")
    if not images_path:
        logger.info("pdf2imamge failed")
        return
    logger.info(f"convert document {file_address} to image success")
    return PptConvertResponse(pdf_path=pdf_path, screenshot=images_path)


# tools
def extract_ppt(ppt_file: str, extract_folder: str = "extracted_pptx") -> None:
    with zipfile.ZipFile(ppt_file, "r") as zip_ref:
        zip_ref.extractall(extract_folder)


tag_agent = TagAgent()


async def tag_audio(file_path: str) -> tuple[str, str]:
    desp = tag_agent.transcribe_audio(file_path)
    return (await tag_agent.format_description(desp), desp)


async def tag_image(file_path: str) -> tuple[str, str]:
    desp = await tag_agent.describe_image(file_path)
    return (await tag_agent.format_description(desp), desp)


@get_time_async
async def tag_file(file_path: str, file_type: str) -> tuple[str, str]:
    match file_type:
        case "image":
            return await tag_image(file_path)
        case "audio":
            return await tag_audio(file_path)
        case _:
            logger.info("Unsupported file type")
            return ("", "")


@get_time_async
async def query_openai_client():
    try:
        response = await tag_agent.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello, OpenAI!"}],
            max_tokens=5,
        )
        logger.info("API 调用成功:", response)
    except Exception as e:
        logger.error("API 调用失败:", e)


def local_path2url_u(path: Path) -> str | None:
    return f"{FILE_SERVER_PREFIX.rstrip('/')}{path}"


async def ppt_parse(item: PptParseRequest) -> PptResponseModel:
    ppt_file = item.ppt_file
    image_convert_res = doc2img(ppt_file)
    if not image_convert_res:
        logger.info("doc2img failed")
        return PptResponseModel(status="failed", msg="doc2img failed")

    presentation = Presentation(ppt_file)
    save_folder = f"{STATIC_DIR}ppt/extract/{datetime.now().timestamp()}"
    extract_ppt(ppt_file, extract_folder=save_folder)

    docu_info: list[SlideInfo] = []

    progress_bar = tqdm(total=len(presentation.slides), desc="Parsing slides")
    for index, slide in enumerate(presentation.slides, start=1):
        shapes = slide.shapes
        title = None
        if shapes.title is not None:
            title = shapes.title.text

        slide_text: list[str] = [shape.text for shape in shapes if shape.has_text_frame]
        slide_images: list[ImageInfo] = []
        slide_videos: list[AssetInfo] = []
        slide_audios: list[AudioInfo] = []
        notes = (
            getattr(slide.notes_slide.notes_text_frame, "text", None)
            if slide.has_notes_slide
            else None
        )

        logger.info(f"page: {index}")
        for shape_index, shape in enumerate(slide.shapes):
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                image_path = (
                    f"{save_folder}/image_{index}_{shape_index}.{shape.image.ext}"
                )
                with open(image_path, "wb") as f:
                    f.write(shape.image.blob)
                asset_info = ImageInfo(
                    left=shape.left.pt,
                    top=shape.top.pt,
                    width=shape.width.pt,
                    height=shape.height.pt,
                )
                asset_info.update_path(image_path)
                asset_info.auto_complete()
                asset_info.update_tag(
                    await tag_file(file_path=image_path, file_type="image")
                )

                slide_images.append(asset_info)

            if shape.shape_type == MSO_SHAPE_TYPE.MEDIA:
                if shape.media_type == PP_MEDIA_TYPE.MOVIE:
                    slide_videos.append(
                        AssetInfo(
                            left=shape.left.pt,
                            top=shape.top.pt,
                            width=shape.width.pt,
                            height=shape.height.pt,
                        )
                    )
                if shape.media_type == PP_MEDIA_TYPE.SOUND:
                    slide_audios.append(
                        AudioInfo(
                            left=shape.left.pt,
                            top=shape.top.pt,
                            width=shape.width.pt,
                            height=shape.height.pt,
                        )
                    )

        video_paths: list[str] = []
        audio_paths: list[str] = []
        media_xml = f"{save_folder}/ppt/slides/_rels/slide{index}.xml.rels"
        media_tree = ET.parse(media_xml)
        for child in media_tree.getroot():
            attrib_type = child.attrib["Type"].split("/")[-1]
            attrib_name = child.attrib["Target"].split("/")[-1]
            if attrib_type == "video":
                video_paths.append(f"{save_folder}/ppt/media/{attrib_name}")
            elif attrib_type == "audio":
                audio_paths.append(f"{save_folder}/ppt/media/{attrib_name}")
        for i, video_path in enumerate(video_paths):
            slide_videos[i].update_path(video_path)
        logger.info(f"slide_audios: {slide_audios}")
        logger.info(f"audio_paths: {audio_paths}")
        # warning:may be not parse audio from pptx lib
        if len(audio_paths) > len(slide_audios):
            slide_audios = []
            for audio_path in audio_paths:
                slide_audio = AudioInfo()
                slide_audio.update_path(audio_path)
                _tag = await tag_file(file_path=audio_path, file_type="audio")
                slide_audio.update_tag(_tag)
                slide_audio.auto_complete()
                slide_audios.append(slide_audio)
        else:
            for i, audio_path in enumerate(audio_paths):
                slide_audios[i].update_path(audio_path)
                _tag = await tag_file(file_path=audio_path, file_type="audio")
                slide_audios[i].update_tag(_tag)
                slide_audios[i].auto_complete()

        if index > len(image_convert_res.screenshot):
            logger.info("pages not eq image counts")
            return PptResponseModel(
                status="failed", code=50001, msg="ppt pages not eq to images"
            )

        slide_info = SlideInfo(
            title=title,
            page=index,
            text=slide_text,
            images=slide_images,
            audios=slide_audios,
            videos=slide_videos,
            notes=notes,
            screenshot=str(image_convert_res.screenshot[index - 1]),
        )
        docu_info.append(slide_info)
        _ = progress_bar.update(1)
    logger.info("ppt parsed")

    return PptResponseModel(
        msg="parse ppt finished",
        result=PptInfo(
            document_info=[slide for slide in docu_info],
            pdf_url=local_path2url_u(image_convert_res.pdf_path),
        ),
    )


def slide_filter(slide: SlideInfo) -> SlideInfo:
    filter_images = [img for img in slide.images if img.use_in_game]
    filter_audios = [aud for aud in slide.audios if aud.use_in_game]
    filter_videos = [vid for vid in slide.videos if vid.use_in_game]
    new_slide = SlideInfo(
        page=slide.page,
        title=slide.title,
        text=slide.text,
        images=filter_images,
        audios=filter_audios,
        videos=filter_videos,
        notes=slide.notes,
        module_id=slide.module_id,
        screenshot=slide.screenshot,
    )
    return new_slide


@get_time_sync
def module_filter(slide_list: PptSlideList) -> PptSlideList:
    new_module_info: list[SlideInfo] = [
        slide_filter(slide) for slide in slide_list.root
    ]
    return PptSlideList(root=new_module_info)


@get_time_sync
def ppt_filter(ppt_info: PptInfo) -> PptInfo:
    new_document_info: list[SlideInfo] = list()
    for slide in ppt_info.document_info:
        if slide.page == 0:
            continue
        new_document_info.append(slide_filter(slide))
    return PptInfo(document_info=new_document_info, pdf_url=ppt_info.pdf_url)


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    encoding = encoding_for_model(model)
    return len(encoding.encode(text))


def update_attach_status(
    id: int,
    status: str,
) -> bool:
    if auth_token is None:
        logger.error("invalid auth token")
        return False
    payload = {"id": id, "status": status}
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }
    response = requests.post(
        f"{GATEWAY}/attach/update_status", json=payload, headers=headers
    )
    if response.status_code != 200:
        logger.error(f"request failed: {response.text = }")
        return False
    response_json = GatewayResponse.model_validate(response.json())
    if response_json.code != 200:
        logger.error(f"request failed: {response_json = }")
        return False
    return True


def query_attach_status(
    id: int,
) -> str | None:
    if auth_token is None:
        logger.error("invalid auth token")
        return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }
    response = requests.get(
        f"{GATEWAY}/attach?file_type=ppt&&attach_id={id}", headers=headers
    )
    if response.status_code != 200:
        logger.error(f"request error: {response.text}")
        return None
    response_json = FileListResponse.model_validate(response.json())
    if response_json.code != 200:
        logger.error(f"request error: {response.text}")
        return None
    if len(response_json.result) == 0:
        logger.error(f"empty result: {response_json = }")
        return None
    return response_json.result[0].status


def create_game(attach_id: int, status: str, module_id: int, file_key: str) -> bool:
    if auth_token is None:
        logger.error("invalid auth token")
        return False
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }
    payload = {
        "attach_id": attach_id,
        "status": status,
        "module_id": module_id,
        "file_key": file_key,
    }
    logger.info(f"creating a new game:\n {payload}")
    response = requests.post(f"{GATEWAY}/game/create", json=payload, headers=headers)
    if response.status_code != 200:
        logger.error(f"create game failed: {response.text}")
        return False
    response_json = GatewayResponse.model_validate(response.json())
    if response_json.code != 200:
        logger.error(f"create game failed: {response_json.msg}")
        return False
    return True


def update_game_status(id: int, status: str, access_url: str | None = None) -> bool:
    if auth_token is None:
        logger.error("invalid auth token")
        return False
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }
    payload = {"id": id, "status": status, "access_url": access_url}
    response = requests.post(
        f"{GATEWAY}/game/update_status", json=payload, headers=headers
    )
    if response.status_code != 200:
        logger.error(f"update status failed: {response.text}")
        return False
    response_json = GatewayResponse.model_validate(response.json())
    if response_json.code != 200:
        logger.error(f"update status failed: {response_json.msg}")
        return False
    return True


def query_game_status(
    id: int,
) -> str | None:
    if auth_token is None:
        logger.error("invalid auth token")
        return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_token,
    }
    response = requests.get(f"{GATEWAY}/game/query?id={id}", headers=headers)
    if response.status_code != 200:
        logger.error(f"request error: {response.text}")
        return None
    response_json = GameListResponse.model_validate(response.json())
    if response_json.code != 200:
        logger.error(f"request error: {response.text}")
        return None
    if len(response_json.result) == 0:
        logger.error(f"empty result: {response_json = }")
        return None
    return response_json.result[0].status


def delete_game_by_attach_id(
    id: int,
) -> bool:
    if auth_token is None:
        logger.error("invalid auth token")
        return False
    headers = {
        "Authorization": auth_token,
    }
    response = requests.delete(f"{GATEWAY}/game?attach_id={id}", headers=headers)
    if response.status_code != 200:
        logger.error(f"request error: {response.text}")
        return False
    logger.info(f"game for attach id {id} has been deleted")
    return True


def feedback_desp(feedback: FeedbackType) -> str:
    match feedback:
        case FeedbackType.SANDBOX_DEBUG:
            return "Sandbox 运行代码反馈信息"
        case FeedbackType.SCREENSHOT:
            return "编译后的游戏截图"
        case _:
            return "用户反馈"


def from_ppt_slide_list(slide_list: PptSlideList) -> LlmSlideList:
    return LlmSlideList(
        root=[LlmSlideInfo.from_slide(slide) for slide in slide_list.root]
    )
