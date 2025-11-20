# AI TTS Studio - Detailed Walkthrough

This document provides a comprehensive overview of the **AI TTS Studio** project, a CLI tool that transforms user prompts into spoken audio using Claude 4.5 Sonnet and ElevenLabs.

## 1. Project Overview

The goal of this project is to create a seamless "text-to-audio" experience where a user provides a high-level prompt (e.g., "Tell me a joke"), and the system:
1.  **Generates a Script**: Uses a Large Language Model (Claude) to write a script optimized for speech.
2.  **Synthesizes Audio**: Uses a Text-to-Speech engine (ElevenLabs) to voice that script.
3.  **Plays Audio**: Immediately plays the result to the user.

## 2. Architecture

The application is structured into modular components to ensure separation of concerns and testability.

```
src/
├── main.py           # Orchestrator: Handles user input and ties components together.
├── llm_client.py     # Intelligence: Interfaces with Anthropic's Claude API.
├── tts_client.py     # Voice: Interfaces with ElevenLabs API.
└── audio_player.py   # Output: Handles audio playback on macOS.
```

### Key Components

#### `LLMClient` (`src/llm_client.py`)
- **Purpose**: Wraps the `anthropic` SDK.
- **Model**: Uses `claude-4-5-sonnet-20251022`.
- **System Prompt**: Configured to act as a "professional scriptwriter", ensuring output is natural and devoid of stage directions (like `[laughs]`), which TTS engines might read aloud.

#### `TTSClient` (`src/tts_client.py`)
- **Purpose**: Wraps the `elevenlabs` SDK.
- **Voice**: Defaults to "Rachel" (Voice ID: `21m00Tcm4TlvDq8ikWAM`), a popular and clear voice.
- **Model**: Uses `eleven_monolingual_v1` for reliable English synthesis.
- **Output**: Streams audio chunks and saves them to a temporary MP3 file.

#### `audio_player` (`src/audio_player.py`)
- **Purpose**: Provides a simple interface to play audio.
- **Implementation**: Uses Python's `subprocess` to call the native macOS `afplay` command. This avoids heavy dependencies like `pyaudio` or `pygame` for simple playback tasks.

## 3. Setup & Configuration

### Dependencies
The project relies on a few key Python packages, listed in `requirements.txt`:
- `anthropic`: For Claude API access.
- `elevenlabs`: For TTS generation.
- `python-dotenv`: For secure API key management.
- `pytest`: For the testing suite.

### Environment Variables
Security is handled via a `.env` file (not committed to git).
- `ANTHROPIC_API_KEY`: Required for script generation.
- `ELEVENLABS_API_KEY`: Required for audio synthesis.

## 4. Usage Flow

1.  **Initialization**: The app checks for API keys and initializes the clients.
2.  **Input Loop**: The user is prompted for input.
3.  **Processing**:
    - The prompt is sent to `LLMClient.generate_script()`.
    - The returned text is displayed.
    - The text is sent to `TTSClient.generate_audio()`.
    - The audio file path is returned.
4.  **Playback**: `play_audio()` is called with the file path.
5.  **Repeat**: The loop continues until the user types 'q'.

## 5. Verification

The project includes a robust test suite in the `tests/` directory.

### Automated Tests (`pytest`)
- **Unit Tests**: `test_llm.py` and `test_tts.py` use `unittest.mock` to simulate API responses. This ensures logic is correct without spending API credits or requiring network access.
- **Integration Tests**: `test_integration.py` mocks the APIs but verifies that the components pass data correctly between each other (LLM output -> TTS input).

### Manual Verification
Verified on macOS:
- [x] Application starts and loads keys.
- [x] Claude generates relevant scripts.
- [x] ElevenLabs generates valid MP3 files.
- [x] Audio plays clearly through system speakers.
- [x] Graceful exit on 'q'.

## 6. Future Improvements

- **Voice Selection**: Allow users to pick a voice from the CLI.
- **Streaming Audio**: Play audio chunks as they arrive for lower latency.
- **Save History**: Save generated scripts and audio files to a `output/` directory.
