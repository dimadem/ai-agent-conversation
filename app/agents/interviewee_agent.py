from agents import Agent
from app.agents.tools.answer_question import answer_question

def create_interviewee_agent(system_prompt: str) -> Agent:
    """Create interviewee agent with provided system prompt."""
    return Agent(
        name="Interviewee Agent",
        handoff_description="Interviewee agent that answers questions based on the persona and skill being tested.",
        instructions=system_prompt,
        tools=[answer_question],
    )

