import unittest
from io import BytesIO
from unittest.mock import MagicMock, mock_open, patch

from src.isolate_voice.isolate_voice import isolate_voice


class TestIsolateVoice(unittest.TestCase):
    def setUp(self):
        """Set up common test variables."""
        self.api_key = "test_api_key"
        self.file_path = "input/test_audio.mp3"
        self.mock_audio_data = b"dummy audio data"

    @patch("src.isolate_voice.isolate_voice.ElevenLabs")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy_audio_data")
    @patch("builtins.print")
    def test_isolate_voice_success_with_bytes(
        self, mock_print, mock_file, mock_elevenlabs
    ):
        """Tests successful voice isolation when the API returns bytes."""
        mock_client = MagicMock()
        mock_elevenlabs.return_value = mock_client
        mock_client.audio_isolation.convert.return_value = b"isolated_audio"

        result = isolate_voice(self.file_path, self.api_key)

        self.assertIsInstance(result, BytesIO)
        self.assertEqual(result.read(), b"isolated_audio")
        mock_file.assert_called_once_with(self.file_path, "rb")
        mock_client.audio_isolation.convert.assert_called_once()
        mock_print.assert_any_call("Voice isolation successful.")

    @patch("src.isolate_voice.isolate_voice.ElevenLabs")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy_audio_data")
    @patch("builtins.print")
    def test_isolate_voice_success_with_filelike(
        self, mock_print, mock_file, mock_elevenlabs
    ):
        """Tests successful voice isolation when the API returns a file-like object."""
        mock_client = MagicMock()
        mock_elevenlabs.return_value = mock_client
        mock_client.audio_isolation.convert.return_value = BytesIO(
            b"isolated_audio_stream"
        )

        result = isolate_voice(self.file_path, self.api_key)

        self.assertIsInstance(result, BytesIO)
        self.assertEqual(result.read(), b"isolated_audio_stream")

    @patch("src.isolate_voice.isolate_voice.ElevenLabs")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy_audio_data")
    @patch("builtins.print")
    def test_isolate_voice_success_with_iterator(
        self, mock_print, mock_file, mock_elevenlabs
    ):
        """Tests successful voice isolation when the API returns an iterator."""
        mock_client = MagicMock()
        mock_elevenlabs.return_value = mock_client
        mock_client.audio_isolation.convert.return_value = iter(
            [b"iso", b"lated_", b"audio"]
        )

        result = isolate_voice(self.file_path, self.api_key)

        self.assertIsInstance(result, BytesIO)
        self.assertEqual(result.read(), b"isolated_audio")

    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_isolate_voice_file_not_found(self, mock_print, mock_open):
        """Tests that None is returned when the file is not found."""
        result = isolate_voice(self.file_path, self.api_key)
        self.assertIsNone(result)
        mock_print.assert_any_call(f"Error: File not found at {self.file_path}")

    @patch("src.isolate_voice.isolate_voice.ElevenLabs")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy_audio_data")
    @patch("builtins.print")
    def test_isolate_voice_api_error(self, mock_print, mock_file, mock_elevenlabs):
        """Tests that None is returned on an API error."""
        mock_client = MagicMock()
        mock_elevenlabs.return_value = mock_client
        mock_client.audio_isolation.convert.side_effect = Exception("API Failure")

        result = isolate_voice(self.file_path, self.api_key)

        self.assertIsNone(result)
        mock_print.assert_any_call("An unexpected error occurred: API Failure")

    @patch("src.isolate_voice.isolate_voice.ElevenLabs")
    @patch("builtins.open", new_callable=mock_open, read_data=b"dummy_audio_data")
    @patch("builtins.print")
    def test_isolate_voice_unsupported_return_type(
        self, mock_print, mock_file, mock_elevenlabs
    ):
        """Tests that None is returned for an unsupported API return type."""
        mock_client = MagicMock()
        mock_elevenlabs.return_value = mock_client
        mock_client.audio_isolation.convert.return_value = (
            12345  # Not bytes, file-like, or iterator
        )

        result = isolate_voice(self.file_path, self.api_key)

        self.assertIsNone(result)
        mock_print.assert_any_call(
            "Voice isolation failed or returned unsupported type."
        )
