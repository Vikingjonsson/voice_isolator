import unittest
from unittest.mock import patch

from src.select_audio_file.select_audio_file import select_audio_file


class TestSelectAudioFile(unittest.TestCase):
    @patch("src.select_audio_file.select_audio_file.find_audio_files", return_value=[])
    @patch("builtins.print")
    def test_select_audio_file_no_files(self, mock_print, mock_find_files):
        """Tests the case where no audio files are found."""
        result = select_audio_file()
        self.assertIsNone(result)
        mock_find_files.assert_called_once_with("input")
        mock_print.assert_any_call("No audio files found in the 'input' directory.")

    @patch(
        "src.select_audio_file.select_audio_file.find_audio_files",
        return_value=["input/single.mp3"],
    )
    @patch("builtins.print")
    def test_select_audio_file_single_file(self, mock_print, mock_find_files):
        """Tests the case where one audio file is found."""
        result = select_audio_file()
        self.assertEqual(result, "input/single.mp3")
        mock_find_files.assert_called_once_with("input")
        mock_print.assert_any_call("Found one audio file: input/single.mp3")

    @patch(
        "src.select_audio_file.select_audio_file.find_audio_files",
        return_value=["input/a.mp3", "input/b.wav"],
    )
    @patch(
        "src.select_audio_file.select_audio_file.prompt_user_for_selection",
        return_value="input/b.wav",
    )
    def test_select_audio_file_multiple_files(self, mock_prompt, mock_find_files):
        """Tests the case where multiple audio files are found."""
        result = select_audio_file()
        self.assertEqual(result, "input/b.wav")
        mock_find_files.assert_called_once_with("input")
        mock_prompt.assert_called_once_with(["input/a.mp3", "input/b.wav"])
