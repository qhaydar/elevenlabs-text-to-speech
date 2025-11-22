import os
import uuid
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

class TTSClient:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        self.client = ElevenLabs(api_key=self.api_key)

    def generate_audio(self, text: str, output_path: str = None) -> str:
        """
        Generates audio from text using ElevenLabs and saves it to a file.
        Returns the path to the saved audio file.
        """
        if not output_path:
            output_path = f"output_{uuid.uuid4()}.mp3"

        # Using a default voice ID (Rachel) - can be parameterized if needed
        # Rachel voice ID: 21m00Tcm4TlvDq8ikWAM
        audio_generator = self.client.generate(
            text=text,
            voice="Rachel",
            model="eleven_monolingual_v1"
        )

        with open(output_path, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        return output_path
