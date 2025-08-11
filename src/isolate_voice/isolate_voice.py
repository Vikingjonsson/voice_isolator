import os
from collections.abc import Iterator
from io import BytesIO
from typing import Union

from elevenlabs.client import ElevenLabs


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

        if isinstance(sdk_result, (bytes, bytearray)):
            buf = BytesIO(bytes(sdk_result))
        elif hasattr(sdk_result, "read"):
            buf = BytesIO(sdk_result.read())
        elif isinstance(sdk_result, Iterator):
            buf = BytesIO()
            for chunk in sdk_result:
                if chunk:
                    buf.write(chunk)
            buf.seek(0)
        else:
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
