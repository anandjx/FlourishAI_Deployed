# flourish_ai/tools/visualizer.py

import json
import base64
from io import BytesIO
import matplotlib.pyplot as plt

def generate_progress_graph(data_json: str) -> str:
    """
    Generates a base64 encoded PNG image of the student's progress graph.
    This simulates the Code Execution feature.
    
    Args:
        data_json: A JSON string containing performance data (e.g., [{'day': 1, 'score': 75}, ...]).
        
    Returns:
        A string containing the base64 encoded image or an error message.
    """
    try:
        data = json.loads(data_json)
        if not data:
            return "Error: No data provided to generate graph."

        days = [d['day'] for d in data]
        scores = [d['score'] for d in data]

        plt.figure(figsize=(6, 4))
        plt.plot(days, scores, marker='o', linestyle='-', color='#4CAF50')
        plt.title('Student Mastery Score Over Time', fontsize=12)
        plt.xlabel('Day', fontsize=10)
        plt.ylabel('Mastery Score (%)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.ylim(0, 100)

        # Save the plot to a buffer
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close() # Close the figure to free memory

        # Encode to Base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return f"SUCCESS_IMAGE_BASE64:{image_base64}"
    
    except json.JSONDecodeError:
        return "Error: Input data must be a valid JSON string containing list of objects."
    except Exception as e:
        return f"An unexpected error occurred during graph generation: {e}"