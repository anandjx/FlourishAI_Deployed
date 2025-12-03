# flourish_ai/tools/memory_bank.py

import json
import os
import random
import string
from datetime import datetime

MEMORY_FILE = "flourish_data_store.json"

def initialize_store():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({}, f)

def generate_unique_student_id() -> str:
    """Generates a unique, readable 5-character code (e.g., 'NOVA9')."""
    initialize_store()
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        new_id = ''.join(random.choices(chars, k=5))
        try:
            with open(MEMORY_FILE, 'r') as f:
                data = json.load(f)
            if new_id not in data: return new_id
        except: return new_id 

def get_cumulative_tokens(student_id: str) -> int:
    initialize_store()
    try:
        with open(MEMORY_FILE, 'r') as f: data = json.load(f)
        return data.get(student_id, {}).get("metrics", {}).get("total_tokens_used", 0)
    except: return 0

def update_cumulative_tokens(student_id: str, tokens_added: int) -> int:
    initialize_store()
    try:
        with open(MEMORY_FILE, 'r') as f: store = json.load(f)
        if student_id not in store: store[student_id] = {"profile": {}, "history": [], "metrics": {"total_tokens_used": 0}}
        
        current = store[student_id].get("metrics", {}).get("total_tokens_used", 0)
        new_total = current + tokens_added
        
        if "metrics" not in store[student_id]: store[student_id]["metrics"] = {}
        store[student_id]["metrics"]["total_tokens_used"] = new_total
        
        with open(MEMORY_FILE, 'w') as f: json.dump(store, f, indent=2)
        return new_total
    except: return 0

# --- CONTEXT COMPACTION LOGIC ---
def read_profile(student_id: str) -> str:
    """
    Retrieves a COMPACTED version of the student's data.
    It returns the full profile but ONLY the last 3 history items.
    """
    initialize_store()
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
        
        user_data = data.get(student_id, {})
        if not user_data:
            return "" 
        
        # --- COMPACTION: Slice history to last 3 events ---
        full_history = user_data.get("history", [])
        compact_history = full_history[-3:] if len(full_history) > 3 else full_history
        
        # Create a view for the agent
        compact_view = {
            "profile": user_data.get("profile", {}),
            "recent_history": compact_history # Only send recent context
        }
        
        return json.dumps(compact_view, indent=2)
    except Exception as e:
        return f"Error: {e}"

def save_profile(student_id: str, profile_data_json: str) -> str:
    initialize_store()
    try:
        if isinstance(profile_data_json, str):
            new_data = json.loads(profile_data_json)
        else:
            new_data = profile_data_json 

        with open(MEMORY_FILE, 'r') as f:
            store = json.load(f)
        
        if student_id not in store:
            store[student_id] = {"profile": {}, "history": [], "metrics": {}}
            
        # Update profile fields
        if "profile" not in store[student_id]: store[student_id]["profile"] = {}
        store[student_id]["profile"].update(new_data)
        
        # Add to history (Infinite log, read_profile handles the compaction)
        if "history" not in store[student_id]: store[student_id]["history"] = []
        
        # Create a concise log entry
        log_entry = {
            "timestamp": datetime.now().strftime("%H:%M"),
            "event": "Update",
            "data_keys": list(new_data.keys())
        }
        store[student_id]["history"].append(log_entry)
        
        with open(MEMORY_FILE, 'w') as f:
            json.dump(store, f, indent=2)
            
        return f"SUCCESS: Profile saved for ID {student_id}"
    except Exception as e:
        return f"Error saving: {e}"