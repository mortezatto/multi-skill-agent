from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field

class RouterOutput(BaseModel):
    """Structured output from the routing node"""
    skills: List[str] = Field(
        description="List of detected skills. Can be empty, 1, or maximum 2 skills.",
        max_length=2
    )
    reasoning: str = Field(description="Short explanation why these skills were chosen")

class AgentState(TypedDict):
    """The state that flows through the LangGraph"""
    user_input: str
    detected_skills: List[str]
    reasoning: str
    skill_results: dict          # will store results of each skill
    final_response: Optional[str]