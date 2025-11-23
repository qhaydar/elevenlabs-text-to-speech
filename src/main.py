import os
import sys
from src.llm_client import LLMClient
from src.tts_client import TTSClient
from src.audio_player import play_audio

def main():
    print("--- AI TTS Studio ---")
    
    # Check for API keys
    if not os.getenv("ANTHROPIC_API_KEY") or not os.getenv("ELEVENLABS_API_KEY"):
        print("Error: API keys not found. Please set ANTHROPIC_API_KEY and ELEVENLABS_API_KEY in your .env file.")
        print("You can copy .env.example to .env and fill in your keys.")
        sys.exit(1)

    try:
        llm_client = LLMClient()
        tts_client = TTSClient()
    except Exception as e:
        print(f"Error initializing clients: {e}")
        sys.exit(1)

    while True:
        try:
            user_prompt = input("\nEnter your prompt (or 'q' to quit): ").strip()
            if user_prompt.lower() == 'q':
                break
            if not user_prompt:
                continue

            print("\nGenerating script with Claude...")
            script = llm_client.generate_script(user_prompt)
            print(f"\n--- Generated Script ---\n{script}\n------------------------")

            print("\nGenerating audio with ElevenLabs...")
            audio_file = tts_client.generate_audio(script)
            print(f"Audio saved to: {audio_file}")

            print("Playing audio...")
            play_audio(audio_file)
            
            # Optional: Clean up audio file
            # os.remove(audio_file)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
