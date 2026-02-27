import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Use Environment Variables for Render (Best Practice)
# If testing locally, ensure these strings are inside "quotes"
SUPABASE_URL = os.getenv("SUPABASE_URL") or "https://mzzjdgxbnzniniiuflan.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or "sb_publishable_jh8ZYqjy_wVhTr0XdsQIeQ_-VtR6i0w"

# FIXED: Added quotes and proper variable usage
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_medication(user_id, name, dosage, time):
    data = {
        "user_id": user_id,
        "med_name": name,
        "dosage": dosage,
        "reminder_time": str(time),
        "status": "active"
    }
    return supabase.table("medications").insert(data).execute()

def get_user_meds(user_id):
    response = supabase.table("medications").select("*").eq("user_id", user_id).execute()
    return response.data