# flourish_ai/tools/__init__.py

# Expose functions from memory_bank.py
from .memory_bank import (
    save_profile, 
    read_profile, 
    get_cumulative_tokens, 
    update_cumulative_tokens, 
    generate_unique_student_id
)

# Expose function from visualizer.py
from .visualizer import generate_progress_graph

# Define what is available when 'from tools import *' is used
__all__ = [
    'save_profile',
    'read_profile',
    'generate_progress_graph',
    'get_cumulative_tokens',
    'update_cumulative_tokens',
    'generate_unique_student_id'  # <--- NEW FUNCTION EXPORTED
]