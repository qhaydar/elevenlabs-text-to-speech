import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate_script(self, prompt: str) -> str:
        """
        Generates a spoken script from a user prompt using Claude 4.5 Sonnet.
        """
        system_prompt = (
            "You are a professional scriptwriter. Convert the following user prompt "
            "into a natural, engaging spoken script suitable for text-to-speech. "
            "Do not include stage directions, just the text to be spoken."
        )

        message = self.client.messages.create(
            model="claude-4-5-sonnet-20251022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
