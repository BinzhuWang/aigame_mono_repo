# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generate_audio_lib.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/14 23:22:38 by dfine             #+#    #+#              #
#    Updated: 2025/05/14 23:22:41 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel

from tools import FILE_SERVER_PREFIX
from tools.definitions import get_audio_info
from tools.wrap_funcs import get_time_sync


class AudioInfo(BaseModel):
    name: str
    url: str
    duration: float
    tag: list[str]


class AudioLibrary(BaseModel):
    audio_library: list[AudioInfo]


@get_time_sync
@lru_cache
def generate_lib(audio_dir: Path) -> AudioLibrary:
    audio_list: list[AudioInfo] = []
    for audio in audio_dir.rglob("*"):
        if not audio.is_file():
            continue
        if audio.suffix.lower() not in [".mp3", ".wav", ".flac", ".ogg"]:
            continue
        _sample_rate, _channels, duration = get_audio_info(str(audio))
        if duration == 0.0:
            continue
        name = audio.stem
        url = f"{FILE_SERVER_PREFIX.rstrip('/')}{audio.absolute()}"
        tags = [tag.strip().replace("_", "") for tag in name.split("-") if tag.strip()]
        audio_info = AudioInfo(name=name, url=url, duration=duration, tag=tags)
        audio_list.append(audio_info)
    return AudioLibrary(audio_library=audio_list)
