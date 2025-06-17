# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tag_agent.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/03 11:13:30 by dfine             #+#    #+#              #
#    Updated: 2025/04/11 11:33:54 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import base64
from copy import deepcopy

from faster_whisper import WhisperModel
from loguru import logger
from openai import AsyncOpenAI, Timeout
from openai.types.chat import (
    ChatCompletionContentPartImageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_content_part_image_param import ImageURL

from . import OPENAI_API_KEY, OPENAI_BASE_URL, TAG_MODEL


class TagAgent:
    client: AsyncOpenAI
    describe_prompt: str
    caption_prompt: str
    format_example: list[ChatCompletionMessageParam]
    trans_model = WhisperModel("models/faster-whisper-tiny")

    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.__init_prompts()

    def __init_prompts(self) -> None:
        with open("prompts/caption.p", "r", encoding="utf-8") as f:
            self.caption_prompt = f.read()
        with open("prompts/describe.p", "r", encoding="utf-8") as f:
            self.describe_prompt = f.read()
        self.format_example = [
            ChatCompletionSystemMessageParam(role="system", content=self.caption_prompt)
        ]
        self.client = AsyncOpenAI(
            api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL, timeout=Timeout(600)
        )

    async def describe_image(self, img_path: str):
        with open(img_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")
        user_content: list[ChatCompletionContentPartParam] = [
            ChatCompletionContentPartTextParam(
                type="text", text="please describe this image content"
            ),
            ChatCompletionContentPartImageParam(
                type="image_url",
                image_url=ImageURL(
                    url=f"data:image/jpeg;base64,{base64_image}", detail="high"
                ),
            ),
        ]
        messages: list[ChatCompletionMessageParam] = [
            ChatCompletionSystemMessageParam(
                role="system", content=self.describe_prompt
            ),
            ChatCompletionUserMessageParam(role="user", content=user_content),
        ]
        response = await self.client.chat.completions.create(
            model=TAG_MODEL,
            temperature=0.2,
            messages=messages,
            max_tokens=300,
        )

        # logger.info(f"response: {response}")
        return response.choices[0].message.content or ""

    def transcribe_audio(self, audio_path: str) -> str:
        logger.info(f"transcript {audio_path}")
        segments, info = self.trans_model.transcribe(audio_path)
        transcript = ""
        for segment in segments:
            logger.info(
                "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
            )
            transcript += segment.text
        # stream = await self.client.audio.transcriptions.create(
        #     model="whisper-1",
        #     file=audio_bytes,
        #     response_format="text",
        #     stream=True,
        # )
        # transcript = ""
        # async for event in stream:
        #     logger.info(f"event type: {event.type}")
        #     if event.type == "transcript.text.delta":
        #         logger.info(event.delta, end="", flush=True)
        #         transcript += event.delta
        logger.info("transcript: ", transcript)
        return transcript

    async def format_description(self, description: str) -> str:
        if len(description) == 0:
            logger.info("No description provided")
            return ""
        messages = deepcopy(self.format_example)
        messages.append(
            ChatCompletionUserMessageParam(role="user", content=description)
        )
        response = await self.client.chat.completions.create(
            model=TAG_MODEL,
            temperature=0.2,
            messages=messages,
        )
        return response.choices[0].message.content or ""
