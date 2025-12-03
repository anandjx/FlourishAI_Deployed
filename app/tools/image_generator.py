# flourish_ai/tools/image_generator.py

import os
import uuid
import base64
import re
from io import BytesIO
from google import genai
from PIL import Image

OUTPUT_DIR = "generated_images"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_educational_image(image_description: str) -> str:
    try:
        client = genai.Client()
        full_prompt = f"Create a clear, high-quality educational illustration or diagram of: {image_description}. Ensure text is legible. Style: Textbook illustration."
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image", 
            contents=[full_prompt],
        )
        
        for part in response.parts:
            if part.inline_data is not None:
                image = part.as_image()
                filename = f"{uuid.uuid4().hex[:8]}.png"
                file_path = os.path.join(OUTPUT_DIR, filename)
                image.save(file_path)
                
                # RETURN PLACEHOLDER
                return f"<<<IMG_FILE:{filename}>>>"
                
        return "Error: No image data returned."
    except Exception as e:
        return f"Error generating image: {str(e)}"

def inject_base64_images(text: str) -> str:
    if not text: return text
    
    pattern = r"<<<IMG_FILE:(.*?)>>>"
    matches = re.findall(pattern, text)
    
    for filename in matches:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(file_path):
            try:
                with Image.open(file_path) as img:
                    img.thumbnail((512, 512)) 
                    buffered = BytesIO()
                    img = img.convert("RGB")
                    img.save(buffered, format="JPEG", quality=80)
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    
                    md_tag = f"![Visual Aid](data:image/jpeg;base64,{img_str})"
                    text = text.replace(f"<<<IMG_FILE:{filename}>>>", md_tag)
            except Exception as e:
                print(f"Failed to inject image {filename}: {e}")
    
    return text