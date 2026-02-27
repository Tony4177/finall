import streamlit as st
from db_utils import supabase

def sign_up(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        return res
    except Exception as e:
        st.error(f"Signup failed: {e}")

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = res.user
        return res
    except Exception as e:
        st.error(f"Login failed: {e}")

def reset_password(email):
    # This sends a reset link to the user's email
    return supabase.auth.reset_password_for_email(email)