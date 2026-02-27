import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Ensure we get the key from Render environment
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    print("❌ Error: GEMINI_API_KEY not found")

# UPDATED: Adding 'models/' prefix often resolves 404 errors in v1beta
model = genai.GenerativeModel('models/gemini-1.5-flash')

def extract_meds_from_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        
        prompt = """
        Analyze this prescription image. Extract:
        1. Medicine Name
        2. Dosage
        3. Frequency/Time
        Format as a clean list.
        """
        
        # 
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        # This will catch if the model name is still causing issues
        return f"Error processing image: {str(e)}"
