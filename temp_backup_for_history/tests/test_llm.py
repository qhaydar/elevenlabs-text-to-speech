import pytest
from unittest.mock import MagicMock, patch
from src.llm_client import LLMClient

@pytest.fixture
def mock_anthropic():
    with patch('src.llm_client.anthropic.Anthropic') as mock:
        yield mock

@patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'fake_key'})
def test_llm_client_initialization(mock_anthropic):
    client = LLMClient()
    assert client.client is not None
    mock_anthropic.assert_called_once_with(api_key='fake_key')

@patch.dict('os.environ', {}, clear=True)
def test_llm_client_missing_key():
    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
        LLMClient()

@patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'fake_key'})
def test_generate_script(mock_anthropic):
    mock_instance = mock_anthropic.return_value
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text="Generated script")]
    mock_instance.messages.create.return_value = mock_message

    client = LLMClient()
    script = client.generate_script("Test prompt")

    assert script == "Generated script"
    mock_instance.messages.create.assert_called_once()
    call_args = mock_instance.messages.create.call_args
    assert call_args.kwargs['model'] == "claude-4-5-sonnet-20251022"
