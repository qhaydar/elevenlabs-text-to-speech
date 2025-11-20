import pytest
from unittest.mock import MagicMock, patch
from src.llm_client import LLMClient
from src.tts_client import TTSClient

@patch('src.llm_client.anthropic.Anthropic')
@patch('src.tts_client.ElevenLabs')
@patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'fake', 'ELEVENLABS_API_KEY': 'fake'})
def test_full_flow(mock_elevenlabs, mock_anthropic):
    # Setup LLM mock
    mock_llm_instance = mock_anthropic.return_value
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Generated script")]
    mock_llm_instance.messages.create.return_value = mock_message

    # Setup TTS mock
    mock_tts_instance = mock_elevenlabs.return_value
    mock_tts_instance.generate.return_value = [b'audio_data']

    # Run flow
    llm_client = LLMClient()
    tts_client = TTSClient()

    script = llm_client.generate_script("Prompt")
    assert script == "Generated script"

    with patch('builtins.open', MagicMock()) as mock_file:
        audio_path = tts_client.generate_audio(script, "test.mp3")
        assert audio_path == "test.mp3"
