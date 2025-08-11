import os
import unittest
from unittest.mock import patch

from src.voice_isolator import get_api_key


class TestGetApiKey(unittest.TestCase):
    @patch.dict(os.environ, {"elevenlabs_api_key": "test_api_key"})
    def test_get_api_key_success(self):
        """Tests that the API key is returned correctly when set."""
        self.assertEqual(get_api_key(), "test_api_key")

    @patch("src.voice_isolator.load_dotenv")
    @patch.dict(os.environ, {}, clear=True)
    def test_get_api_key_not_found(self, mock_load_dotenv):
        """Tests that a ValueError is raised when the API key is not found."""
        with self.assertRaises(ValueError):
            get_api_key()
