import unittest
from unittest.mock import patch, mock_open
from io import BytesIO

from src.voice_isolator import save_result


class TestSaveResult(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_save_result_with_bytes(self, mock_print, mock_file):
        """Tests saving audio data provided as bytes."""
        audio_data = b"some_audio_data"
        original_path = "input/source_audio.wav"
        expected_output_path = "output/source_audio_isolated.mp3"

        save_result(audio_data, original_path)

        mock_file.assert_called_once_with(expected_output_path, "wb")
        mock_file().write.assert_called_once_with(audio_data)
        mock_print.assert_called_once_with(
            f"Cleaned audio saved as: {expected_output_path}"
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_save_result_with_bytesio(self, mock_print, mock_file):
        """Tests saving audio data provided as a BytesIO object."""
        audio_data = BytesIO(b"some_audio_in_a_stream")
        original_path = "/another/path/to/a/song.flac"
        expected_output_path = "output/song_isolated.mp3"

        save_result(audio_data, original_path)

        mock_file.assert_called_once_with(expected_output_path, "wb")
        mock_file().write.assert_called_once_with(b"some_audio_in_a_stream")
        mock_print.assert_called_once_with(
            f"Cleaned audio saved as: {expected_output_path}"
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_save_result_with_different_extension(self, mock_print, mock_file):
        """Tests that the output extension is always .mp3."""
        audio_data = b"data"
        original_path = "input/file.m4a"
        expected_output_path = "output/file_isolated.mp3"

        save_result(audio_data, original_path)

        mock_file.assert_called_once_with(expected_output_path, "wb")
        mock_file().write.assert_called_once_with(audio_data)