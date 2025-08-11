import unittest
from unittest.mock import patch

from src.voice_isolator import select_audio_file


class TestSelectAudioFile(unittest.TestCase):
    @patch("src.voice_isolator.glob.glob", return_value=[])
    @patch("builtins.print")
    def test_no_audio_files_found(self, mock_print, mock_glob):
        """Tests that None is returned when no audio files are found."""
        self.assertIsNone(select_audio_file())
        mock_print.assert_any_call("No audio files found in the 'input' directory.")

    @patch(
        "src.voice_isolator.glob.glob",
        side_effect=[["input/test.mp3"], [], [], []],
    )
    @patch("builtins.print")
    def test_single_audio_file_found(self, mock_print, mock_glob):
        """Tests that the single audio file is returned without a prompt."""
        result = select_audio_file()
        self.assertEqual(result, "input/test.mp3")
        mock_print.assert_any_call("Found one audio file: input/test.mp3")

    @patch(
        "src.voice_isolator.glob.glob",
        side_effect=[["input/test.mp3", "input/anothertest.wav"], [], [], []],
    )
    @patch("builtins.input", return_value="2")
    @patch("builtins.print")
    def test_multiple_audio_files_found_valid_choice(
        self, mock_print, mock_input, mock_glob
    ):
        """Tests that the correct file is returned with multiple files and valid user input."""
        result = select_audio_file()
        self.assertEqual(result, "input/anothertest.wav")
        mock_input.assert_called_once_with("Enter your choice (1-2): ")

    @patch(
        "src.voice_isolator.glob.glob",
        side_effect=[["input/test.mp3", "input/anothertest.wav"], [], [], []],
    )
    @patch("builtins.input", side_effect=["3", "1"])
    @patch("builtins.print")
    def test_multiple_audio_files_found_invalid_then_valid_choice(
        self, mock_print, mock_input, mock_glob
    ):
        """Tests that the function handles invalid and then valid user input."""
        result = select_audio_file()
        self.assertEqual(result, "input/test.mp3")
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_any_call("Invalid choice. Please try again.")

    @patch(
        "src.voice_isolator.glob.glob",
        side_effect=[["input/test.mp3", "input/anothertest.wav"], [], [], []],
    )
    @patch("builtins.input", side_effect=["abc", "2"])
    @patch("builtins.print")
    def test_multiple_audio_files_found_non_numeric_choice(
        self, mock_print, mock_input, mock_glob
    ):
        """Tests that the function handles non-numeric user input."""
        result = select_audio_file()
        self.assertEqual(result, "input/anothertest.wav")
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_any_call("Invalid input. Please enter a number.")
