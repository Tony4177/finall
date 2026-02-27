import openai
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Get your key from your Render Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq provides an OpenAI-compatible API
client = openai.OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def ask_ai_assistant(user_query, med_history):
    # Convert medication data into a readable string for context
    meds_context = ""
    if med_history:
        meds_context = ", ".join([f"{m['med_name']} ({m['dosage']}) at {m['reminder_time']}" for m in med_history])
    else:
        meds_context = "No medications currently scheduled."

    system_prompt = f"""
    You are a professional and friendly Medicine Reminder Assistant. 
    The user's current medications: {meds_context}.
    
    Rules:
    1. Help the user understand how to take their meds correctly.
    2. Give general health advice based on their specific meds.
    3. IMPORTANT: Always include a disclaimer that you are an AI and they should consult a doctor.
    4. Keep answers short and easy to read.
    """
    
    try:
        # UPDATED: Using llama-3.1-8b-instant for speed and reliability
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.5 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I'm having trouble connecting to my brain right now. Error: {e}"
