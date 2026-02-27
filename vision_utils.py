import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from Render/System
load_dotenv()

# Get the key and verify it exists
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # This will show up in your Render 'Logs' if the key is missing
    print("CRITICAL ERROR: GEMINI_API_KEY is not set in Environment Variables!")
else:
    # Configure Gemini with the retrieved key
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.0-flash')

def extract_meds_from_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        
        prompt = """
        Analyze this prescription image. Extract the following details for each medicine:
        1. Medicine Name
        2. Dosage (e.g., 500mg)
        3. Frequency/Time (e.g., 9:00 AM, twice a day)
        
        Format the output as a clean list. If you are unsure, say 'Manual check required'.
        """
        
        # 
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error processing image: {str(e)}"
