import glob
import os

from src.constants import SUPPORTED_FORMATS


def find_audio_files(directory: str) -> list[str]:
    """Finds all supported audio files in a directory."""
    print(f"Searching for audio files in '{directory}/' directory...")
    audio_files: list[str] = []
    for file_format in SUPPORTED_FORMATS:
        audio_files.extend(
            glob.glob(os.path.join(directory, file_format), recursive=True)
        )
    return audio_files
