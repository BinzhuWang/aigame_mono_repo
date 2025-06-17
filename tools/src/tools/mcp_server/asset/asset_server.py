from pathlib import Path
from uuid import uuid4

from mcp.server.fastmcp import FastMCP

from .image_gen import generate_image
from .tts import MsConfig, MsText
from . import ASSET_SERVER_PREFIX

server = FastMCP("Assets Generate Server")


@server.tool()
async def audio_generate(text: str) -> str:
    """
    Generates an audio file from the provided text using Text-to-Speech (TTS) conversion.

    This function takes a string of text, converts it into speech using the TTS system,
    and saves the resulting audio file as a `.wav` file.

    If the specified directory does not exist, it will be automatically created.
    A unique filename for the audio file will be generated using a UUID to avoid overwriting existing files.

    Parameters:
    - text (str): The text that will be converted into audio.

    Returns:
    - str: The url address to the saved audio file.
    """

    save_path = Path("/data/upload/assets/audio/")
    save_path.mkdir(parents=True, exist_ok=True)
    ms_config = MsConfig()
    ms_text = MsText(content=text)
    audio_bytes = ms_config.ssml_tts(ms_text.ssml())
    audio_path = save_path / f"{uuid4()}.wav"
    with open(audio_path, "wb") as f:
        _ = f.write(audio_bytes)
    return str(f"{ASSET_SERVER_PREFIX}{audio_path}")


@server.tool()
async def image_generate(prompt: str) -> list[str]:
    """
    Generates one or more images based on the given textual prompt.

    This function uses an image generation engine (such as a diffusion model or other AI-based renderer)
    to create visual content from a provided prompt. The generated images are saved to the specified directory.
    If the specified directory does not exist, it will be automatically created.

    If image generation fails or no images are returned, an empty list is returned instead.

    Parameters:
    - prompt (str): A textual description of the image(s) to generate. This could include visual elements, styles, or scenes.

    Returns:
    - list[str]: A list of url address(as strings) to the successfully generated image files.
    """
    res = generate_image(prompt, Path(f"/data/upload/assets/image/{uuid4()}"))
    if not res.succeed or not res.path:
        return []
    return [f"{ASSET_SERVER_PREFIX}{p}" for p in res.path]


if __name__ == "__main__":
    server.run()
