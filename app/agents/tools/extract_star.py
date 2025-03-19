from app.model.ttt import TTT
from agents import function_tool

from typing import List
from pydantic import BaseModel

ttt = TTT()

class Message(BaseModel):
    role: str
    content: str

extract_star_components_json = {
            "name": "extract_star_components",
            "description": "Extract STAR elements from an interview transcript and return structured data. Do not invent anything, use only a given interview transcript",
            "parameters": {
                "type": "object",
                "properties": {
                    "Situation": {"type": "string", "description": "Extracted situation from the interview. If the situation is not specified do not invent it, just tell there is no situation described."},
                    "Task": {"type": "string", "description": "Extracted task from the interview. If the task is not specified do not invent it, just tell there is no task described."},
                    "Action": {"type": "string", "description": "Extracted action from the interview. If the action is not specified do not invent it, just tell there is no action described."},
                    "Result": {"type": "string", "description": "Extracted result from the interview. If the result is not specified do not invent it, just tell there is no result described."}
                },
                "required": ["Situation", "Task", "Action", "Result"]
            }
        }

@function_tool
def extract_star_components(messages: List[Message]) -> dict:
    """
    Extract STAR elements from an interview transcript and return structured data. Do not invent anything, use only a given interview transcript.

    Args:
        messages (list): A list of messages from the interview transcript. Each message is a dictionary containing 'role' and 'content'.

    Return:
        "Situation": {"type": "string", "description": "Extracted situation from the interview. If the situation is not specified do not invent it, just tell there is no situation described."},
        "Task": {"type": "string", "description": "Extracted task from the interview. If the task is not specified do not invent it, just tell there is no task described."},
        "Action": {"type": "string", "description": "Extracted action from the interview. If the action is not specified do not invent it, just tell there is no action described."},
        "Result": {"type": "string", "description": "Extracted result from the interview. If the result is not specified do not invent it, just tell there is no result described."}
    """

    response = ttt.generate_response_with_function(
        messages=messages,
        functions=[extract_star_components_json],
        tool={"name": "extract_star_components"}
    )
    print("Response from extract_star_components:", response)
    return response