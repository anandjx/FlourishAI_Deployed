# flourish_ai/agent.py

import logging
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.genai.types import Content, Part

# --- IMPORTS ---
from .tools.memory_bank import save_profile, read_profile, get_cumulative_tokens, update_cumulative_tokens
from .tools.visualizer import generate_progress_graph 
from .tools.image_generator import inject_base64_images # Import Image Injector

# Sub-Agents
from .sub_agents.Flourish_Curriculum_Agent.agent import curriculum_agent
from .sub_agents.Flourish_Pedagogical_Critic.agent import critic_agent
from .sub_agents.Flourish_Vision_Grader.agent import vision_agent 
from .sub_agents.Flourish_Analytics_Reporter.agent import analytics_agent 
from .sub_agents.Flourish_User_Profiler.agent import profiler_agent
from .sub_agents.Flourish_Assessment_Agent.agent import assessment_agent
from .sub_agents.Flourish_Visual_Teacher.agent import visual_agent

from .prompt import ORCHESTRATOR_PROMPT, ORCHESTRATOR_OUTPUT_KEY

# --- MASTER CALLBACK (IMAGES + TOKENS) ---
def master_callback(callback_context, llm_response):
    """
    1. Injects Images (Swaps placeholders for Base64).
    2. Tracks Tokens (Adds session footer).
    """
    try:
        # 1. Skip if it's a Tool Call (we don't modify internal traffic)
        if hasattr(llm_response, 'content') and llm_response.content.parts:
            for part in llm_response.content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    return None

        # 2. Process Content
        if hasattr(llm_response, 'content') and llm_response.content.parts:
            
            # --- STEP A: INJECT IMAGES ---
            if hasattr(llm_response.content.parts[0], 'text'):
                original_text = llm_response.content.parts[0].text
                # This function looks for <<<IMG_FILE:x>>> and swaps it for the real image
                processed_text = inject_base64_images(original_text)
                llm_response.content.parts[0].text = processed_text

            # --- STEP B: ADD TOKEN FOOTER ---
            usage = getattr(llm_response, 'usage_metadata', None) or getattr(getattr(llm_response, 'content', None), 'usage_metadata', None)
            
            if usage:
                # Calculate session total
                current_total = update_cumulative_tokens("current_session", usage.total_token_count)
                
                footer = f"\n\n<sub>*💎 Tokens: In {usage.prompt_token_count} | Out {usage.candidates_token_count} | Session: {current_total}*</sub>"
                
                # Append footer (check if we already added it to avoid duplicates)
                if hasattr(llm_response.content.parts[0], 'text'):
                    if "Session:" not in llm_response.content.parts[0].text:
                        llm_response.content.parts[0].text += footer

    except Exception as e:
        print(f"UI Processing failed: {e}")

    return None

# --- TOOL WRAPPING ---
memory_read_tool = FunctionTool(read_profile)
memory_save_tool = FunctionTool(save_profile)
visualizer_tool = FunctionTool(generate_progress_graph)

# --- SUB-AGENT HELPER FUNCTIONS ---
# We define these helper functions to allow the Orchestrator to call the sub-agents.
# FunctionTool uses the type hints (user_query: str) to explain the tool to the LLM.

def call_curriculum_agent(user_query: str) -> str:
    """Delegates a query to the Curriculum Agent."""
    response = curriculum_agent.query(user_query)
    return getattr(response, 'answer', str(response))

def call_critic_agent(user_query: str) -> str:
    """Delegates a query to the Pedagogical Critic Agent."""
    response = critic_agent.query(user_query)
    return getattr(response, 'answer', str(response))

def call_vision_agent(user_query: str) -> str:
    """Delegates a query to the Vision Grader Agent."""
    response = vision_agent.query(user_query)
    return getattr(response, 'answer', str(response))

def call_analytics_agent(user_query: str) -> str:
    """Delegates a query to the Analytics Reporter Agent."""
    response = analytics_agent.query(user_query)
    return getattr(response, 'answer', str(response))

def call_profiler_agent(user_query: str) -> str:
    """Delegates a query to the User Profiler Agent."""
    response = profiler_agent.query(user_query)
    return getattr(response, 'answer', str(response))

def call_assessment_agent(user_query: str) -> str:
    """Delegates a query to the Assessment Agent."""
    response = assessment_agent.query(user_query)
    return getattr(response, 'answer', str(response))

def call_visual_agent(user_query: str) -> str:
    """Delegates a query to the Visual Teacher Agent."""
    response = visual_agent.query(user_query)
    return getattr(response, 'answer', str(response))


# --- AGENT TOOLS ---
# Wrap the helpers with FunctionTool so the Orchestrator can use them
curriculum_tool = FunctionTool(call_curriculum_agent)
critic_tool = FunctionTool(call_critic_agent)
vision_tool = FunctionTool(call_vision_agent)
analytics_tool = FunctionTool(call_analytics_agent)
profiler_tool = FunctionTool(call_profiler_agent)
assessment_tool = FunctionTool(call_assessment_agent)
visual_tool = FunctionTool(call_visual_agent)


# --- ROOT AGENT DEFINITION ---

flourish_orchestrator = LlmAgent(
    model="gemini-2.5-flash", 
    name="FlourishAI_Orchestrator",
    description="The root agent for FlourishAI.",
    instruction=ORCHESTRATOR_PROMPT,
    output_key=ORCHESTRATOR_OUTPUT_KEY,
    after_model_callback=master_callback, # Use the combined callback
    tools=[
        profiler_tool,
        curriculum_tool, 
        critic_tool,
        vision_tool,    
        analytics_tool,
        assessment_tool,
        visual_tool,
        memory_read_tool,
        memory_save_tool,
        visualizer_tool
    ]
)

root_agent = flourish_orchestrator