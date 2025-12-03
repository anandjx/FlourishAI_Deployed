# flourish_ai/sub_agents/Flourish_Curriculum_Agent/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool, google_search
from . import prompt

# NOTE: We do NOT import image_generator here to avoid conflicts with google_search.
# The Visual Teacher agent handles images.

MODEL = "gemini-2.5-flash"

curriculum_agent = LlmAgent(
    model=MODEL,
    name="Flourish_Curriculum_Agent",
    instruction=prompt.CURRICULUM_AGENT_PROMPT,
    output_key=prompt.CURRICULUM_OUTPUT_KEY,
    description="Generates lessons and researches topics using Google Search.",
    tools=[google_search] # Only Google Search here
)