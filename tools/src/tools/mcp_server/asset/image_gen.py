import requests
from pathlib import Path
from time import sleep
from pydantic import BaseModel, HttpUrl
from . import FAL_API_KEY, FAL_API_URL


class GenerateResponseModel(BaseModel):
    status: str
    request_id: str
    response_url: HttpUrl
    status_url: HttpUrl
    cancel_url: HttpUrl
    logs: str | None = None
    metrics: dict[str, str | int | float]
    queue_position: int | None = None


class ImageInfo(BaseModel):
    url: HttpUrl
    width: int
    height: int
    content_type: str


class ImageResultResponse(BaseModel):
    images: list[ImageInfo]


class ResponseModel(BaseModel):
    succeed: bool = True
    msg: str
    path: list[str] | None = None


def response_err(msg: str) -> ResponseModel:
    return ResponseModel(succeed=False, msg=msg)


def generate_image(prompt: str, save_dir: Path) -> ResponseModel:
    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json",
    }

    print(headers)
    response = requests.post(FAL_API_URL, json={"prompt": prompt}, headers=headers)
    if response.status_code != 200:
        return response_err(f"request failed: {response.text}")
    response_json = GenerateResponseModel.model_validate(response.json())
    print(response_json)
    status_url = f"{FAL_API_URL}/requests/{response_json.request_id}/status"
    status_headers = {
        "Authorization": f"Key {FAL_API_KEY}",
    }
    while True:
        status_response = requests.get(status_url, headers=status_headers)
        # if status_response.status_code != 200:
        #     return response_err(
        #         f"cannot query {response_json.request_id} status, code: {status_response.status_code} response: {status_response.text}"
        #     )
        status_json = GenerateResponseModel.model_validate(status_response.json())
        if status_json.status == "COMPLETED":
            request_image_url = f"{FAL_API_URL}/requests/{response_json.request_id}"
            image_response = requests.get(request_image_url, headers=status_headers)
            if image_response.status_code != 200:
                return response_err(
                    f"cannot get image url, response: {image_response.text}"
                )
            image_json = ImageResultResponse.model_validate(image_response.json())
            save_dir.mkdir(parents=True, exist_ok=True)
            path_list: list[str] = []
            for index, image_info in enumerate(image_json.images):
                image_response = requests.get(
                    str(image_info.url), headers=status_headers
                )
                if image_response.status_code != 200:
                    return response_err(f"cannot download image from {image_info.url}")
                image_path = save_dir / f"{index}.jpg"
                with open(image_path, "wb") as f:
                    _ = f.write(image_response.content)
                    print(f"saved image to {image_path}")
                    path_list.append(str(image_path))
            return ResponseModel(msg="image generated succeed", path=path_list)
        elif status_json.status == "FAILED":
            return response_err("image generating failed")
        else:
            print("waiting for image generating")
            sleep(3)
