import glob
import os
from io import BytesIO
from typing import Union

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


def get_api_key() -> str:
    """Loads the ElevenLabs API key from .env file."""
    load_dotenv()
    api_key = os.getenv("elevenlabs_api_key")
    if not api_key:
        raise ValueError(
            "API key not found. Please create a .env file and add your elevenlabs_api_key."
        )
    return api_key


def select_audio_file() -> Union[str, None]:
    """Finds audio files and prompts the user to select one."""
    print("Searching for audio files in 'input/' directory...")
    SUPPORTED_FORMATS = ["**/*.mp3", "**/*.wav", "**/*.flac", "**/*.m4a"]
    audio_files: list[str] = []
    for file_format in SUPPORTED_FORMATS:
        audio_files.extend(
            glob.glob(os.path.join("input", file_format), recursive=True)
        )

    if not audio_files:
        print("No audio files found in the 'input' directory.")
        print("Please add your audio files to the 'input' folder.")
        return None

    if len(audio_files) == 1:
        print(f"Found one audio file: {audio_files[0]}")
        return audio_files[0]

    print("Multiple audio files found. Please select one:")
    for i, file_path in enumerate(audio_files):
        print(f"{i + 1}: {os.path.basename(file_path)}")

    while True:
        try:
            choice = int(input(f"Enter your choice (1-{len(audio_files)}): "))
            if 1 <= choice <= len(audio_files):
                return audio_files[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def isolate_voice(file_path: str, api_key: str) -> Union[BytesIO, None]:
    """Sends the audio file to ElevenLabs for voice isolation using the official SDK.
    Always returns a BytesIO stream on success, regardless of the SDK's return form.
    """
    print(f"Processing '{os.path.basename(file_path)}' for voice isolation...")
    try:
        elevenlabs = ElevenLabs(api_key=api_key)
        with open(file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        sdk_result = elevenlabs.audio_isolation.convert(audio=BytesIO(audio_data))

        # Normalize to BytesIO: handle bytes, file-like, or iterator of bytes
        if isinstance(sdk_result, (bytes, bytearray)):
            buf = BytesIO(bytes(sdk_result))
        elif hasattr(sdk_result, "read"):
            # file-like object
            buf = BytesIO(sdk_result.read())
        else:
            try:
                iterator = iter(sdk_result)
                buf = BytesIO()
                for chunk in iterator:
                    if not chunk:
                        continue
                    buf.write(chunk)
                buf.seek(0)
            except TypeError:
                print("Voice isolation failed or returned unsupported type.")
                return None

        print("Voice isolation successful.")
        return buf
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def save_result(audio_data: Union[bytes, BytesIO], original_path: str):
    """Saves the isolated audio to the output directory."""
    original_filename = os.path.basename(original_path)
    name, ext = os.path.splitext(original_filename)
    output_filename = f"{name}_isolated.mp3"
    output_path = os.path.join("output", output_filename)

    # Accept either bytes or a BytesIO-like object
    data_to_write = (
        audio_data.getvalue() if hasattr(audio_data, "getvalue") else audio_data
    )
    with open(output_path, "wb") as f:
        f.write(data_to_write)
    print(f"Cleaned audio saved as: {output_path}")
