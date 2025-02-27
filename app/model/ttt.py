from typing import Dict, List, Union
from app.core.yandex import sdk
from app.core.config import YANDEX_FOLDER_ID

class TTT:
    def __init__(self, model: str = f"gpt://{YANDEX_FOLDER_ID}/yandexgpt/rc"):
        self.sdk = sdk
        self.model = model

    def generate_response(self, messages: Union[Dict, List[Dict]]) -> str:
        """
        Generate text response using Yandex API
        """
        try:
            if not isinstance(messages, list):
                messages = [messages]
            
            completion = self.sdk.models.completions(self.model).configure(temperature=0.0, reasoning_mode='DISABLED').run(messages)
            print(completion)
            return completion[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def create_message(self, role: str, text: str) -> Dict[str, str]:
        """
        Create chat message in Yandex API format
        """
        return {
            "role": role,
            "text": text
        }