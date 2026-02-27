import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Get the key from Render environment
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_meds_from_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        
        # We try the most stable naming convention first
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = """
        Analyze this prescription image. Extract:
        1. Medicine Name
        2. Dosage
        3. Frequency/Time
        Format as a clean list. If you cannot read it, say 'Manual check required'.
        """
        
        response = model.generate_content([prompt, image])
        return response.text
        
    except Exception as e:
        # Fallback for 404 errors: Try the versioned name
        try:
            model_fallback = genai.GenerativeModel('gemini-1.5-flash')
            response = model_fallback.generate_content([prompt, image])
            return response.text
        except Exception as e2:
            return f"AI Error: Please ensure your GEMINI_API_KEY is correct in Render. ({str(e2)})"
