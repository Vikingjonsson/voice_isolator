import unittest
from unittest.mock import patch

from src.select_audio_file.prompt_user_for_selection.prompt_user_for_selection import (
    prompt_user_for_selection,
)


class TestPromptUserForSelection(unittest.TestCase):
    def setUp(self):
        self.audio_files = ["input/test1.mp3", "input/test2.wav"]

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_prompt_user_valid_choice(self, mock_print, mock_input):
        """Tests that a valid user choice is handled correctly."""
        result = prompt_user_for_selection(self.audio_files)
        self.assertEqual(result, "input/test1.mp3")
        mock_input.assert_called_once_with("Enter your choice (1-2): ")

    @patch("builtins.input", side_effect=["3", "2"])
    @patch("builtins.print")
    def test_prompt_user_invalid_then_valid_choice(self, mock_print, mock_input):
        """Tests handling of an out-of-range choice followed by a valid one."""
        result = prompt_user_for_selection(self.audio_files)
        self.assertEqual(result, "input/test2.wav")
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_any_call("Invalid choice. Please try again.")

    @patch("builtins.input", side_effect=["abc", "1"])
    @patch("builtins.print")
    def test_prompt_user_non_numeric_then_valid_choice(self, mock_print, mock_input):
        """Tests handling of non-numeric input followed by a valid one."""
        result = prompt_user_for_selection(self.audio_files)
        self.assertEqual(result, "input/test1.mp3")
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_any_call("Invalid input. Please enter a number.")
