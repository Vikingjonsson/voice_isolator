from src.get_api_key import get_api_key
from src.isolate_voice import isolate_voice
from src.save_result import save_result
from src.select_audio_file import select_audio_file


def main():
    """Main function to run the voice isolation process."""
    try:
        api_key = get_api_key()
        audio_file_path = select_audio_file()

        if audio_file_path:
            isolated_audio = isolate_voice(audio_file_path, api_key)
            if isolated_audio:
                save_result(isolated_audio, audio_file_path)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
