import subprocess
import os

def play_audio(file_path: str):
    """
    Plays an audio file using the native macOS 'afplay' command.
    """
    if not os.path.exists(file_path):
        print(f"Error: Audio file not found at {file_path}")
        return

    try:
        subprocess.call(['afplay', file_path])
    except FileNotFoundError:
        print("Error: 'afplay' command not found. Are you on macOS?")
    except Exception as e:
        print(f"Error playing audio: {e}")
