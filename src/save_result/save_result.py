import os
from io import BytesIO
from typing import Union


def save_result(audio_data: Union[bytes, BytesIO], original_path: str):
    """Saves the isolated audio to the output directory."""
    original_filename = os.path.basename(original_path)
    name, ext = os.path.splitext(original_filename)
    output_filename = f"{name}_isolated.mp3"
    output_path = os.path.join("output", output_filename)

    data_to_write = (
        audio_data.getvalue() if hasattr(audio_data, "getvalue") else audio_data
    )
    with open(output_path, "wb") as f:
        f.write(data_to_write)
    print(f"Cleaned audio saved as: {output_path}")
