from app.model.ttt import TTT

from agents import function_tool

from typing import List
from pydantic import BaseModel

ttt = TTT()

class Message(BaseModel):
    role: str
    content: str

@function_tool
def answer_question(messages: List[Message]) -> str:
    """
    Generates a brief interviewee response based on the persona and skill being tested. Behave naturally.
    The function uses the TTT model to generate a response based on the provided messages.

    Arguments:
        messages: List of messages to be processed.
    
    Return:
        response: The interviewee's response.
    """
    response = ttt.generate_response(messages)
    return response