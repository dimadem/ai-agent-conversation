from typing import List, Dict
from app.core.openai import client

class TTT:
    def __init__(self, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate text response
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def create_chat_message(self, role: str, content: str) -> Dict[str, str]:
        """
        Create chat message with role and content
        """
        return {
            "role": role,
            "content": content
        }

