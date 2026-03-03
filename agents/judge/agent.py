from typing import Literal

from google.adk.agents import Agent
from pydantic import BaseModel, Field

MODEL = "gemini-2.5-pro"


# JudgeFeedback Schema
# It extends BaseModel and define 'status' ("pass" or "fail") and 'feedback'.
# This class defines the structure for feedback returned by the Judge agent.
class JudgeFeedback(BaseModel):
    """Structured feedback from the Judge agent."""

    # Status field can only be "pass" or "fail" to indicate evaluation result
    status: Literal["pass", "fail"] = Field(
        description="Whether the research is sufficient ('pass') or needs more work ('fail')."
    )
    # Feedback field contains detailed comments about the evaluation
    feedback: str = Field(
        description="Detailed feedback on what is missing. If 'pass', a brief confirmation."
    )


# Judge Agent
# The judge accepts research findings, evaluate them, and output the JudgeFeedback schema.
judge = Agent(
    name="judge",
    model=MODEL,
    description="Evaluates research findings for completeness and accuracy.",
    instruction="""
    You are a strict editor.
    Evaluate the 'research_findings' against the user's original request.
    If the findings are missing key info, return status='fail'.
    If they are comprehensive, return status='pass'.
    """,
    output_schema=JudgeFeedback,
    # Disallow delegation because it should only output the schema
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

root_agent = judge
