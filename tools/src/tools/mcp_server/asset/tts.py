# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tts.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/12 20:37:07 by dfine             #+#    #+#              #
#    Updated: 2025/04/12 20:40:43 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from enum import Enum
from random import choice
from typing import Literal

from loguru import logger
import requests
from edge_tts import Communicate, VoicesManager
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_random

from . import MS_TTS_KEY, MS_TTS_REGION


class VoiceStyle(Enum):
    ADVERTISEMENT_UPBEAT = "advertisement_upbeat"
    AFFECTIONATE = "affectionate"
    ANGRY = "angry"
    ASSISTANT = "assistant"
    CALM = "calm"
    CHAT = "chat"
    CHEERFUL = "cheerful"
    CUSTOMERSERVICE = "customerservice"
    DEPRESSED = "depressed"
    DISGRUNTLED = "disgruntled"
    DOCUMENTARY_NARRATION = "documentary-narration"
    EMBARRASSED = "embarrassed"
    EMPATHETIC = "empathetic"
    ENVIOUS = "envious"
    EXCITED = "excited"
    FEARFUL = "fearful"
    FRIENDLY = "friendly"
    GENTLE = "gentle"
    HOPEFUL = "hopeful"
    LYRICAL = "lyrical"
    NARRATION_PROFESSIONAL = "narration-professional"
    NARRATION_RELAXED = "narration-relaxed"
    NEWSCAST = "newscast"
    NEWSCAST_CASUAL = "newscast-casual"
    NEWSCAST_FORMAL = "newscast-formal"
    POETRY_READING = "poetry-reading"
    SAD = "sad"
    SERIOUS = "serious"
    SHOUTING = "shouting"
    SPORTS_COMMENTARY = "sports_commentary"
    SPORTS_COMMENTARY_EXCITED = "sports_commentary_excited"
    WHISPERING = "whispering"
    TERRIFIED = "terrified"
    UNFRIENDLY = "unfriendly"


class VoiceRole(Enum):
    GIRL = "Girl"
    BOY = "Boy"
    YOUNG_ADULT_FEMALE = "YoungAdultFemale"
    YOUNG_ADULT_MALE = "YoungAdultMale"
    OLDER_ADULT_FEMALE = "OlderAdultFemale"
    OLDER_ADULT_MALE = "OlderAdultMale"
    SENIOR_FEMALE = "SeniorFemale"
    SENIOR_MALE = "SeniorMale"


class VoiceRate(Enum):
    X_SLOW = "x-slow"  # ≈ 0.5, -50%
    SLOW = "slow"  # ≈ 0.64, -46%
    MEDIUM = "medium"  # 1.0, 默认
    FAST = "fast"  # ≈ 1.55, +55%
    X_FAST = "x-fast"  # 2.0, +100%


class VoiceVolume(Enum):
    SILENT = "silent"  # 0.0
    X_SOFT = "x-soft"  # 0.2
    SOFT = "soft"  # 0.4
    MEDIUM = "medium"  # 0.6
    LOUD = "loud"  # 0.8
    X_LOUD = "x-loud"  # 1.0 (默认)


class VoiceEmotion(BaseModel):
    style: VoiceStyle | None
    degree: float | None
    role: VoiceRole | None = None

    def ssml(self) -> str | None:
        if self.style is None and self.degree is None and self.role is None:
            return None
        ssml_text = "<mstts:express-as "
        if self.style:
            ssml_text += f'style="{self.style.value}"'
        if self.role:
            ssml_text += f'role="{self.role.value}"'
        if self.degree:
            ssml_text += f'styledegree="{self.degree}"'

        return ssml_text + ">\n"


class MsText(BaseModel):
    lang: str = "en-US"
    speaker: str = "en-US-AvaMultilingualNeural"
    emotion: VoiceEmotion | None = None
    content: str
    gender: Literal["Male", "Female"] = "Female"
    rate: VoiceRate = VoiceRate.MEDIUM
    volume: VoiceVolume = VoiceVolume.X_LOUD

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random(max=3),
    )
    async def edge(self, save_path: str) -> None:
        voices = await VoicesManager.create()
        logger.info(f"{voices = }")
        voice = voices.find(Gender=self.gender, Locale=self.lang)
        if not voice:
            logger.error("valid voice is empty")
            raise ValueError
        # logger.info(f"valid {voice = }")
        communicate = Communicate(self.content, choice(voice)["Name"])
        await communicate.save(save_path)

    def ssml(self):
        ssml_text = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{self.lang}">\n'
        ssml_text += f'<voice name="{self.speaker}">\n'
        with_emotion_flag = False
        if self.emotion:
            txt = self.emotion.ssml()
            if txt is not None:
                ssml_text += txt
                with_emotion_flag = True
        ssml_text += (
            f'<prosody rate="{self.rate.value}" volume="{self.volume.value}">\n'
        )
        ssml_text += self.content
        ssml_text += "</prosody>\n"
        ssml_text += "</mstts:express-as>\n" if with_emotion_flag else ""
        ssml_text += "</voice>\n</speak>"
        return ssml_text


class MsConfig(BaseModel):
    auth_key: str
    url: str

    def __init__(self, auth_key: str | None = None, region: str | None = None):
        region = region or MS_TTS_REGION
        auth_key = auth_key or MS_TTS_KEY
        url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
        super().__init__(auth_key=auth_key, url=url)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random(max=3),
    )
    def ssml_tts(self, ssml: str) -> bytes:
        if len(ssml) == 0:
            raise ValueError("invalid ssml")
        headers = {
            "Content-Type": "application/ssml+xml",
            "Ocp-Apim-Subscription-Key": f"{self.auth_key}",
            "X-Microsoft-OutputFormat": "riff-44100hz-16bit-mono-pcm",
            "User-Agent": "aigame",
        }
        response = requests.post(
            self.url, headers=headers, data=ssml.encode("utf-8"), timeout=600
        )
        if response.status_code != 200:
            print("TTS failed:", response.status_code, response.text)
            raise RuntimeError("TTS request failed")
        return response.content
