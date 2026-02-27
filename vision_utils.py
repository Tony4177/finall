import google.generativeai as genai
import os
from PIL import Image

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_meds_from_image(uploaded_file):
    image = Image.open(uploaded_file)
    
    prompt = """
    Analyze this prescription image. Extract the following details for each medicine:
    1. Medicine Name
    2. Dosage (e.g., 500mg)
    3. Frequency/Time (e.g., 9:00 AM, twice a day)
    
    Format the output as a clean list. If you are unsure, say 'Manual check required'.
    """
    
    response = model.generate_content([prompt, image])
    return response.text
