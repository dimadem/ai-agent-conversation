from app.model.ttt import TTT 

ttt = TTT()

extract_star_components_json = {
                "name": "extract_star_components",
                "description": "Extract STAR elements from an interview transcript and return structured data. Do not invent anything, use onle a given interview transcript",
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

def extract_star_components(messages):
    response = ttt.generate_response_with_function(
        messages=messages,
        functions=[extract_star_components_json],
        tool={"name": "extract_star_components"}
    )
    return response
