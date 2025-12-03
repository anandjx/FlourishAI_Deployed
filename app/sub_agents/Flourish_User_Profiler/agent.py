# flourish_ai/sub_agents/Flourish_User_Profiler/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import prompt

# Import tools
from app.tools.memory_bank import save_profile, generate_unique_student_id

# Wrap tools
save_profile_tool = FunctionTool(save_profile)
gen_id_tool = FunctionTool(generate_unique_student_id)

MODEL = "gemini-2.0-flash"

profiler_agent = LlmAgent(
    model=MODEL,
    name="Flourish_User_Profiler",
    instruction=prompt.PROFILE_AGENT_PROMPT,
    output_key=prompt.PROFILE_OUTPUT_KEY,
    description="Manages Login and Signup. Generates unique 5-char IDs.",
    tools=[save_profile_tool, gen_id_tool]
)