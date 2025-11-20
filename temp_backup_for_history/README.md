# ElevenLabs Text-to-Speech

A CLI tool that generates spoken scripts from prompts using **Claude 4.5 Sonnet** and converts them to audio using **ElevenLabs**.

## Features

- **Script Generation**: Uses Claude 4.5 Sonnet to convert simple prompts into engaging spoken scripts.
- **Text-to-Speech**: Uses ElevenLabs' high-quality TTS (Rachel voice) to generate audio.
- **Instant Playback**: Automatically plays the generated audio on macOS.

## Prerequisites

- Python 3.8+
- macOS (for `afplay` audio playback)
- API Keys:
    - [Anthropic API Key](https://console.anthropic.com/)
    - [ElevenLabs API Key](https://elevenlabs.io/)

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/qhaydar/elevenlabs-text-to-speech.git
    cd elevenlabs-text-to-speech
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API keys**:
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    - Edit `.env` and add your actual API keys.

## Usage

Run the application:

```bash
python src/main.py
```

1.  Enter a prompt when asked (e.g., "Explain quantum physics like I'm 5").
2.  Wait for Claude to generate the script.
3.  Wait for ElevenLabs to generate the audio.
4.  Listen to the result!

## Testing

Run the test suite:

```bash
pytest
```

## Project Structure

- `src/main.py`: Entry point.
- `src/llm_client.py`: Handles interaction with Claude.
- `src/tts_client.py`: Handles interaction with ElevenLabs.
- `src/audio_player.py`: Handles audio playback.
