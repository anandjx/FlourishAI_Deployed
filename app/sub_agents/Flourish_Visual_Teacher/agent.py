# flourish_ai/sub_agents/Flourish_Visual_Teacher/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import prompt

# Import tools
from app.tools.image_generator import generate_educational_image
from app.tools.memory_bank import read_profile

# Wrap tools
image_tool = FunctionTool(generate_educational_image)
profile_tool = FunctionTool(read_profile)

MODEL = "gemini-2.0-flash"

visual_agent = LlmAgent(
    model=MODEL,
    name="Flourish_Visual_Teacher",
    instruction=prompt.VISUAL_TEACHER_PROMPT,
    output_key=prompt.VISUAL_OUTPUT_KEY,
    description="Generates educational images. Can read profile to find the topic.",
    tools=[image_tool, profile_tool] # Now it has memory!
)