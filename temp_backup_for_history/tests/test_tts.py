import pytest
from unittest.mock import MagicMock, patch, mock_open
from src.tts_client import TTSClient

@pytest.fixture
def mock_elevenlabs():
    with patch('src.tts_client.ElevenLabs') as mock:
        yield mock

@patch.dict('os.environ', {'ELEVENLABS_API_KEY': 'fake_key'})
def test_tts_client_initialization(mock_elevenlabs):
    client = TTSClient()
    assert client.client is not None
    mock_elevenlabs.assert_called_once_with(api_key='fake_key')

@patch.dict('os.environ', {}, clear=True)
def test_tts_client_missing_key():
    with pytest.raises(ValueError, match="ELEVENLABS_API_KEY not found"):
        TTSClient()

@patch.dict('os.environ', {'ELEVENLABS_API_KEY': 'fake_key'})
def test_generate_audio(mock_elevenlabs):
    mock_instance = mock_elevenlabs.return_value
    mock_instance.generate.return_value = [b'chunk1', b'chunk2']

    client = TTSClient()
    
    with patch('builtins.open', mock_open()) as mock_file:
        output_path = client.generate_audio("Test text", "test_output.mp3")
        
        assert output_path == "test_output.mp3"
        mock_instance.generate.assert_called_once_with(
            text="Test text",
            voice="Rachel",
            model="eleven_monolingual_v1"
        )
        mock_file.assert_called_with("test_output.mp3", "wb")
        mock_file().write.assert_any_call(b'chunk1')
        mock_file().write.assert_any_call(b'chunk2')
