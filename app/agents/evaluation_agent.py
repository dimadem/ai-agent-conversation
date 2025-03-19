from agents import Agent
from app.agents.tools.extract_star import extract_star_components
from pydantic import BaseModel


class STAROutput(BaseModel):
    Situation: str
    Task: str
    Action: str
    Result: str

def create_evaluation_agent(system_prompt: str) -> Agent:
    return Agent(
        name="Evaluation Agent",
        handoff_description="Evaluation messages with STAR method.",
        instructions=system_prompt,
        tools=[extract_star_components],
        output_type=STAROutput
    )