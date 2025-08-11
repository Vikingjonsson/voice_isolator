import os
import unittest
from unittest.mock import call, patch

from src.constants import SUPPORTED_FORMATS
from src.select_audio_file.find_audio.find_audio_files import find_audio_files


class TestFindAudioFiles(unittest.TestCase):
    @patch("src.select_audio_file.find_audio.find_audio_files.glob.glob")
    @patch("builtins.print")
    def test_find_audio_files_finds_files(self, mock_print, mock_glob_glob):
        """Tests that audio files are found correctly."""
        mock_glob_glob.side_effect = [["input/test1.mp3"], ["input/test2.wav"], [], []]

        directory = "input"

        result = find_audio_files(directory)

        self.assertEqual(result, ["input/test1.mp3", "input/test2.wav"])

        expected_glob_calls = [
            call(os.path.join(directory, pattern), recursive=True)
            for pattern in SUPPORTED_FORMATS
        ]
        mock_glob_glob.assert_has_calls(expected_glob_calls)

    @patch(
        "src.select_audio_file.find_audio.find_audio_files.glob.glob",
        return_value=[],
    )
    @patch("builtins.print")
    def test_find_audio_files_no_files(self, mock_print, mock_glob_glob):
        """Tests that an empty list is returned when no files are found."""
        directory = "input"
        result = find_audio_files(directory)
        self.assertEqual(result, [])
