from typing import Union

from src.constants import INPUT_DIR
from src.select_audio_file.find_audio.find_audio_files import find_audio_files
from src.select_audio_file.prompt_user_for_selection.prompt_user_for_selection import (
    prompt_user_for_selection,
)


def select_audio_file() -> Union[str, None]:
    """Orchestrates finding and selecting an audio file."""
    audio_files = find_audio_files(INPUT_DIR)

    if not audio_files:
        print(f"No audio files found in the '{INPUT_DIR}' directory.")
        print(f"Please add your audio files to the '{INPUT_DIR}' folder.")
        return None

    if len(audio_files) == 1:
        print(f"Found one audio file: {audio_files[0]}")
        return audio_files[0]

    return prompt_user_for_selection(audio_files)
