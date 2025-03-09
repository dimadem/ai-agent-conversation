from app.model.ttt import TTT

ttt = TTT()

answer_question_json = {
                            "name": "answer_question",
                            "description": "Generates a brief interviewee response based on the persona and skill being tested. Behave naturally",
                            "parameters": 
                            {
                                "type": "object",
                                "properties": 
                                {
                                    "response": 
                                    {
                                        "type": "string", 
                                        "description": "The interviewee's response."
                                    }
                                },
                                "required": ["response"]
                            }
                        }

def interviewee_response(messages):
    response = ttt.generate_response_with_function(
        messages=messages,
        functions=[answer_question_json]
    )
    return response