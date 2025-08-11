import os


def prompt_user_for_selection(audio_files: list[str]) -> str:
    """Prompts the user to select a file from a list and returns the selected path."""
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
