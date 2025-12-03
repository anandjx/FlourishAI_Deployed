# flourish_ai/sub_agents/Flourish_Analytics_Reporter/agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from . import prompt

# --- FIX: Use full package path for the import ---
from app.tools.visualizer import generate_progress_graph 

visualizer_tool = FunctionTool(generate_progress_graph)

MODEL = "gemini-2.0-flash" 

analytics_agent = LlmAgent(
    model=MODEL,
    name="Flourish_Analytics_Reporter",
    instruction=prompt.ANALYTICS_AGENT_PROMPT,
    output_key=prompt.ANALYTICS_OUTPUT_KEY,
    tools=[visualizer_tool] 
)