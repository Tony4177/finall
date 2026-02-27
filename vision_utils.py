import google.generativeai as genai
import os
from PIL import Image

# DIRECT RETRIEVAL: We check for both common names
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    # This will print in your Render 'Logs' tab
    print("❌ ERROR: No API Key found in Render Environment Variables!")
else:
    # Explicitly pass the key into the configuration
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.0-flash')

def extract_meds_from_image(uploaded_file):
    if not api_key:
        return "System Error: Gemini API Key is missing in Render settings."
        
    try:
        image = Image.open(uploaded_file)
        prompt = """
        Analyze this prescription image. Extract:
        1. Medicine Name
        2. Dosage
        3. Frequency/Time
        Format as a clean list.
        """
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error processing image: {str(e)}"
