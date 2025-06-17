# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    runway.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dfine <coding@dfine.tech>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/25 20:05:04 by dfine             #+#    #+#              #
#    Updated: 2025/05/25 20:05:05 by dfine            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from pathlib import Path
import time
from typing import Literal
from runwayml import RunwayML
from runwayml.types import TaskRetrieveResponse
import requests

from tools import FILE_SERVER_PREFIX, RUNWAY_API_KEY, STATIC_DIR

ModelType = Literal["gen4_turbo", "gen3a_turbo"]
ResolutionType = Literal[
    "1280:720",
    "720:1280",
    "1104:832",
    "832:1104",
    "960:960",
    "1584:672",
    "1280:768",
    "768:1280",
]
DurationType = Literal[5, 10]

TaskResponse = TaskRetrieveResponse


class RunwayVideoGenerator:
    def __init__(
        self,
        *,
        api_key: str = RUNWAY_API_KEY,
        timeout: int = 600,
        poll_interval: int = 10,
    ):
        self.client: RunwayML = RunwayML(api_key=api_key)
        self.timeout: int = timeout
        self.poll_interval: int = poll_interval
        self.save_path: Path = Path(STATIC_DIR) / "assets" / "video"
        self.save_path.mkdir(parents=True, exist_ok=True)

    def download(self, task: TaskResponse) -> list[str]:
        if task.status != "SUCCEEDED":
            return []
        if task.output is None:
            return []
        res: list[str] = []
        for i, url in enumerate(task.output):
            try:
                save_path = self.save_path / task.id
                save_path.mkdir(parents=True, exist_ok=True)
                file_name = f"{i}.mp4"
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(save_path / file_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        _ = f.write(chunk)
                res.append(f"{FILE_SERVER_PREFIX.rstrip('/')}{save_path / file_name}")
            except Exception as e:
                print(f"Failed to download {url}: {e}")
        return res

    def generate_video(
        self,
        *,
        image_url: str,
        prompt: str = "Generate a video",
        model: ModelType = "gen4_turbo",
        ratio: ResolutionType = "1280:720",
        duration: DurationType = 5,
    ) -> list[str]:
        task = self.client.image_to_video.create(
            model=model,
            prompt_image=image_url,
            prompt_text=prompt,
            ratio=ratio,
            duration=duration,
        )
        task_id = task.id

        for count in range(0, self.timeout, self.poll_interval):
            time.sleep(self.poll_interval)
            task = self.client.tasks.retrieve(task_id)
            if task.status in ("SUCCEEDED", "FAILED"):
                return self.download(task)
        raise TimeoutError(f"wait too long for video generating, {task_id= }")
