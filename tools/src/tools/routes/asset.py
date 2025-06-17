# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    asset.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/18 13:47:38 by dfine             #+#    #+#              #
#    Updated: 2025/05/18 15:51:04 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from functools import lru_cache
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel

from tools.mcp_server.asset import ASSET_SERVER_PREFIX
from tools.mcp_server.asset.image_gen import generate_image
from tools.mcp_server.asset.tts import MsConfig, MsText
from tools.runway import (
    DurationType,
    ModelType,
    ResolutionType,
    RunwayVideoGenerator,
)
from tools.wrap_funcs import get_time_async

router = APIRouter()

runway_client = RunwayVideoGenerator()


@lru_cache
def audio_config() -> tuple[MsConfig, Path]:
    ms_config = MsConfig()
    audio_save_path = Path("/data/upload/assets/audio/")
    audio_save_path.mkdir(parents=True, exist_ok=True)
    return (ms_config, audio_save_path)


@lru_cache
def image_config() -> Path:
    image_save_path = Path("/data/upload/assets/image/")
    image_save_path.mkdir(parents=True, exist_ok=True)
    return image_save_path


class ResponseModel(BaseModel):
    status: str = "succeed"
    code: int = 200
    msg: str
    result: dict[str, str] | list[str] | None = None


@router.post("/tts")
@get_time_async
async def tts(ms_text: MsText):
    ms_config, audio_save_path = audio_config()
    logger.info(f"{ms_config = }")
    logger.info(f"{ms_text= }")
    logger.info(f"ssml:\n{ms_text.ssml()}")
    audio_path = audio_save_path / f"{uuid4()}.wav"
    try:
        audio_bytes = ms_config.ssml_tts(ms_text.ssml())
        with open(audio_path, "wb") as f:
            _ = f.write(audio_bytes)
    except Exception as e1:
        logger.error(f"failed to generate use azure tts. {e1}")
        logger.warning("use edge-tts to generate audio...")
        try:
            await ms_text.edge(str(audio_path))
            logger.info("generate audio succeed by edge-tts.")
        except Exception as e2:
            logger.error(f"Don't panic, edge-tts also failed. {e2}")
            return ResponseModel(msg=f"tts failed, {e2}")
    return ResponseModel(
        msg="text to speech finished",
        result={"audio": f"{ASSET_SERVER_PREFIX.rstrip('/')}{audio_path}"},
    )


class ImageRequest(BaseModel):
    prompt: str


@router.post("/image/gen")
@get_time_async
async def image_gen(image_request: ImageRequest) -> ResponseModel:
    image_save_path = image_config()
    res = generate_image(image_request.prompt, image_save_path / f"{uuid4()}")
    if not res.succeed or not res.path:
        return ResponseModel(code=500, status="failed", msg="failed to generate image")
    image_list = [f"{ASSET_SERVER_PREFIX.rstrip('/')}{p}" for p in res.path]
    return ResponseModel(msg="image generate finished", result=image_list)


class VideoRequest(BaseModel):
    model: ModelType = "gen4_turbo"
    image_url: str
    prompt_text: str
    ratio: ResolutionType = "1280:720"
    duration: DurationType = 5


@router.post("/video/runway")
@get_time_async
async def runway_gen(video_request: VideoRequest) -> ResponseModel:
    try:
        video_task = runway_client.generate_video(
            image_url=video_request.image_url,
            prompt=video_request.prompt_text,
            model=video_request.model,
            ratio=video_request.ratio,
            duration=video_request.duration,
        )
        return ResponseModel(
            msg="image-to-video task finished, see result for status", result=video_task
        )
    except Exception as e:
        return ResponseModel(
            code=500, status="failed", msg=f"failed to generate image: {e}"
        )
