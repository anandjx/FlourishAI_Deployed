# flourish_ai/sub_agents/Flourish_Assessment_Agent/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from . import prompt

# Use Gemini Pro for complex test generation and evaluation logic
MODEL = "gemini-2.5-flash"

assessment_agent = LlmAgent(
    model=MODEL,
    name="Flourish_Assessment_Agent",
    instruction=prompt.ASSESSMENT_AGENT_PROMPT,
    output_key=prompt.ASSESSMENT_OUTPUT_KEY,
    description="Generates quizzes, mock exams, interviews, and printable tests.",
    tools=[google_search] # Needed for "IQ Tests" or current events quizzes
)