# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    definitions.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/03 11:13:20 by dfine             #+#    #+#              #
#    Updated: 2025/05/14 15:26:07 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from collections.abc import Generator
from pathlib import Path
from typing import Self
from uuid import uuid4

from PIL import Image
from loguru import logger
from pydantic import BaseModel, RootModel
from datetime import datetime
from enum import StrEnum, auto
import base64

from pydub import AudioSegment

from tools.wrap_funcs import get_time_sync

from . import (
    FILE_SERVER_PREFIX,
    RABBITMQ_EXCHANGE,
    RABBITMQ_PARSE_QUEUE,
    RABBITMQ_GEN_QUEUE,
    RABBITMQ_ROUTING_KEY,
    RABBITMQ_URI,
    TMP_DIR,
)


class QueueName(BaseModel):
    ppt_parse: str
    game_generate: str


class MessageConfig(BaseModel):
    exchange_name: str
    queue_name: QueueName
    routing_key: str
    uri: str


message_config = MessageConfig(
    uri=RABBITMQ_URI,
    queue_name=QueueName(
        ppt_parse=RABBITMQ_PARSE_QUEUE, game_generate=RABBITMQ_GEN_QUEUE
    ),
    exchange_name=RABBITMQ_EXCHANGE,
    routing_key=RABBITMQ_ROUTING_KEY,
)


class PptHandlerPayload(BaseModel):
    id: int
    path: str


class GameHandlerPayload(BaseModel):
    id: int
    file_key: str
    module_id: int
    status: str


class Position(BaseModel):
    left: float
    top: float


class Size(BaseModel):
    width: float
    height: float


class MediaInfo(BaseModel):
    position: Position
    size: Size


class AssetInfo(BaseModel):
    path: str = ""
    local_path: str = ""
    left: float = 0.0
    top: float = 0.0
    width: float = 0.0
    height: float = 0.0
    use_in_game: bool = False
    tag: str = ""
    desp: str = ""

    def update_path(self, path: str) -> None:
        self.local_path = path
        self.path = f"{FILE_SERVER_PREFIX}{path}"

    def update_tag(self, tag_info: tuple[str, str]) -> None:
        self.tag, self.desp = tag_info


def get_image_info(file_path: str) -> tuple[int, int]:
    with Image.open(file_path) as img:
        return img.size


def get_audio_info(file_path: str) -> tuple[int, int, float]:
    audio = AudioSegment.from_file(file_path)
    sample_rate = audio.frame_rate
    channels = audio.channels
    duration = len(audio) / 1000.0  # 转换为秒
    return sample_rate, channels, duration


class ImageInfo(AssetInfo):
    ori_width: int = 0
    ori_height: int = 0

    def auto_complete(self):
        try:
            self.ori_width, self.ori_height = get_image_info(self.local_path)
        except Exception as e:
            logger.error(f"failed to get image info: {e}")


class AudioInfo(AssetInfo):
    sample_rate: int = 0
    duration_secs: float = 0.0
    channels: int = 0

    def auto_complete(self):
        try:
            self.sample_rate, self.channels, self.duration_secs = get_audio_info(
                self.local_path
            )
        except Exception as e:
            logger.error(f"failed to get audio info: {e}")


class SlideInfo(BaseModel):
    page: int
    title: str | None
    text: list[str]
    images: list[ImageInfo]
    videos: list[AssetInfo]
    audios: list[AudioInfo]
    notes: str | None = None
    module_id: int | None = None
    screenshot: str


class LlmSlideInfo(BaseModel):
    page: int
    title: str | None
    text: list[str]
    images: list[ImageInfo]
    videos: list[AssetInfo]
    audios: list[AudioInfo]
    notes: str | None = None
    module_id: int | None = None
    screenshot: str

    @classmethod
    def from_slide(cls, slide: SlideInfo) -> Self:
        return cls(
            page=slide.page,
            title=slide.title,
            text=slide.text,
            images=slide.images,
            videos=slide.videos,
            audios=slide.audios,
            notes=slide.notes,
            module_id=slide.module_id,
            screenshot=f"{FILE_SERVER_PREFIX.rstrip('/')}{slide.screenshot}",
        )


PptSlideList = RootModel[list[SlideInfo]]
LlmSlideList = RootModel[list[LlmSlideInfo]]


class PptInfo(BaseModel):
    document_info: list[SlideInfo]
    pdf_url: str | None = None

    @get_time_sync
    def get_a_module(self) -> Generator[tuple[int, PptSlideList], None, None]:
        current_module_id = -1
        slide_list: list[SlideInfo] = []
        for slide in self.document_info:
            if slide.module_id is None:
                return
            if current_module_id == -1:
                current_module_id = slide.module_id
            if current_module_id != slide.module_id:
                yield current_module_id, PptSlideList(slide_list.copy())
                current_module_id = slide.module_id
                slide_list.clear()
            slide_list.append(slide)
        if slide_list:
            yield current_module_id, PptSlideList(slide_list)


class PptConvertResponse(BaseModel):
    pdf_path: Path
    screenshot: list[Path]


class PptResponseModel(BaseModel):
    status: str = "succeed"
    code: int = 200
    msg: str
    result: PptInfo | None = None


class ResponseModel(BaseModel):
    status: str = "succeed"
    code: int = 200
    msg: str
    result: dict[str, str] | None = None


class EvidenceItem(BaseModel):
    page: int
    text_excerpt: str
    image_summary: str | None = ""  # 可为空


class GameAssetModel(BaseModel):
    asset_name: str
    type: str
    prompt: str
    resolution: str | None = None
    duration: str | float | None = None
    fps: int | None = None
    reference: str


class GameKnowledgeModel(BaseModel):
    content: str
    context: str
    page: int


class GameGoalElement(BaseModel):
    module_id: int
    start_page: int
    end_page: int
    game_goal: str
    evidence: list[EvidenceItem] | None = None
    knowledge_list: list[GameKnowledgeModel] | None = None
    asset_list: list[GameAssetModel]


class GameGoalList(BaseModel):
    modules: list[GameGoalElement]


class Step(BaseModel):
    action: str
    response: str


class Feedback(BaseModel):
    success: str
    retry: str


class GameDesignModule(BaseModel):
    module_id: int
    game_name: str
    game_type: str
    instructions: str
    steps: list[Step]
    win_condition: str
    failure_condition: str
    feedback: Feedback
    assets_required: list[str]
    duration_seconds: int
    replayable: bool


class Features(BaseModel):
    core_mechanics: list[str]
    input_logic: list[str]
    ui_elements: list[str]
    animations_assets: list[str]
    audio_feedback: list[str]


class PrototypeFlow(BaseModel):
    state: str
    description: str
    user_input: str
    next_state: str


GameAssetModels = RootModel[list[GameAssetModel]]


class GamePlanModel(BaseModel):
    module_id: int
    game_name: str
    core_gameplay_summary: str
    features: Features
    prototype_flow: list[PrototypeFlow]
    estimated_duration_seconds: int
    asset_list: GameAssetModels
    knowledge_list: list[GameKnowledgeModel] | None = None


class GameTaskElement(BaseModel):
    id: str
    name: str
    description: str
    category: str
    priority: str
    dependencies: list[str]
    estimated_effort_hours: int
    assignee: str


class GameTaskModel(BaseModel):
    module_id: int
    module_name: str
    tasks: list[GameTaskElement]


GameDesignModules = RootModel[list[GameDesignModule]]
GamePlanModels = RootModel[list[GamePlanModel]]
GameTaskModels = RootModel[list[GameTaskModel]]


class GameProjectModel(BaseModel):
    asset_list: GameAssetModels
    plan: GamePlanModel


class GatewayResponse(BaseModel):
    code: int
    msg: str
    result: int | str | None = None


class FileItem(BaseModel):
    """
    Represents a single file item in the result list.
    """

    id: int
    name: str
    created_at: datetime  # Pydantic can automatically parse ISO 8601 strings into datetime objects
    status: str


class FileListResponse(BaseModel):
    """
    Represents the overall response structure for the file list API.
    """

    code: int
    msg: str
    result: list[FileItem]


class GameItem(BaseModel):
    """
    Represents a single file item in the result list.
    """

    id: int
    status: str
    attach_id: int
    module_id: int


class GameListResponse(BaseModel):
    """
    Represents the overall response structure for the file list API.
    """

    code: int
    msg: str
    result: list[GameItem]


class FeedbackType(StrEnum):
    SANDBOX_DEBUG = auto()
    USER_ASK = auto()
    SCREENSHOT = auto()


class ChatContentModel(BaseModel):
    content: str
    feedback_type: FeedbackType

    def convert_b64_to_url(self) -> Self:
        if self.feedback_type == FeedbackType.SCREENSHOT:
            if self.content.startswith("data:image"):
                self.content = self.content.split(",")[1]
            image_data = base64.b64decode(self.content)
            save_dir = Path(TMP_DIR) / "chat_image"
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = save_dir / f"{uuid4()}.png"

            with open(save_path, "wb") as f:
                _ = f.write(image_data)
            self.content = f"{FILE_SERVER_PREFIX.rstrip('/')}/{save_path}"
        return self
