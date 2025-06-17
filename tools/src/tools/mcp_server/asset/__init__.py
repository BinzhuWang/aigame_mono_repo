import os


MS_TTS_KEY = os.getenv("MS_TTS_KEY", "")
MS_TTS_REGION = os.getenv("MS_TTS_REGION", "eastus")
FAL_API_KEY = os.getenv("FAL_API_KEY", "")
FAL_API_URL = os.getenv(
    "FAL_API_URL", "https://queue.fal.run/workflows/Giggle-5tbk7waf2rql/max"
)
ASSET_SERVER_PREFIX = os.getenv("HOST_URL", "https://api.gamecreator.online")
