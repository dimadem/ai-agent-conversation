from pathlib import Path
from app.core.yandex import sdk

class TTS:
    def __init__(self, model: str = "tts-1", voice: str = "alloy"):
        self.client = sdk
        self.model = model
        self.voice = voice

    def generate_speech(self, text: str):
        """
        Generate speech from text using TTS model
        """
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text
            )
            return response
        except Exception as e:
            return f"Error generating speech: {str(e)}"

    def save_to_file(self, text: str, file_path: str | Path) -> bool:
        """
        Generate speech and save to file
        """
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model=self.model,
                voice=self.voice,
                input=text
            ) as response:
                response.stream_to_file(file_path)
            return True
        except Exception as e:
            print(f"Error saving audio file: {str(e)}")
            return False
