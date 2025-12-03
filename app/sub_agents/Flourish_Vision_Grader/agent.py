# flourish_ai/sub_agents/vision/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import prompt

# Placeholder for your custom image processing tool 
# (This function would handle saving results to the database)
def process_vision_data(analysis_json: str) -> str:
    """Takes the Gemini Vision analysis and logs it to the student's record."""
    # Logic to save to Memory Bank will go here
    return f"Vision analysis logged successfully."

vision_logger_tool = FunctionTool(process_vision_data)

# NOTE: The Orchestrator will send the image directly to this agent using Gemini's multimodal input capability.
MODEL = "gemini-2.0-flash" # Essential for multimodal/vision

vision_agent = LlmAgent(
    model=MODEL,
    name="Flourish_Vision_Grader",
    instruction=prompt.VISION_AGENT_PROMPT,
    output_key=prompt.VISION_OUTPUT_KEY,
    tools=[vision_logger_tool] 
)