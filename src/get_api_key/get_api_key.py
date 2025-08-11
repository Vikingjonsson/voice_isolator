import os

from dotenv import load_dotenv


def get_api_key() -> str:
    """Loads the ElevenLabs API key from .env file."""
    load_dotenv()
    api_key = os.getenv("elevenlabs_api_key")
    if not api_key:
        raise ValueError(
            "API key not found. Please create a .env file and add your elevenlabs_api_key."
        )
    return api_key
