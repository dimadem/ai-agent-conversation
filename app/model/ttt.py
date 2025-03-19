from typing import List, Dict, Union, Any
from app.core.openai import client
import json


class TTT:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = client
        self.model = model

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate text response
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return completion.choices[0].message.content

        except Exception as e:
            return f"Error generating response: {str(e)}"
        

    def generate_response_with_function(self, messages: List[Dict[str, str]], functions: List[Dict] = None, tool: Any = None) -> Union[str, Dict]:
        """
        Generate text response with function call
        """
        try:
            # Подготовка параметров запроса
            params = {
                "model": self.model,
                "messages": messages,
            }
            
            # Добавляем functions и function_call только если они предоставлены
            if functions:
                params["functions"] = functions
                
            if tool:
                params["function_call"] = tool
            
            # Выполняем запрос к API
            response = self.client.chat.completions.create(**params)
            message = response.choices[0].message
            
            # Проверяем, содержит ли ответ вызов функции
            if hasattr(message, "function_call") and message.function_call:
                function_args = json.loads(message.function_call.arguments)
                return function_args
            else:
                # Если нет вызова функции, возвращаем текстовый ответ
                return message.content
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