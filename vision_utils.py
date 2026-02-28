from google import genai
import os
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Initialize the new Google GenAI Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        
        # Using Gemini 2.5 Flash, the current stable workhorse
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, image]
        )
        
        return response.text
        
    except Exception as e:
        # If 2.5 Flash fails, try a broader alias as a backup
        try:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=[prompt, image]
            )
            return response.text
        except Exception as e2:
            return f"System Error: {str(e2)}"
