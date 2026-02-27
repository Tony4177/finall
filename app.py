import streamlit as st
import datetime
import time
from auth_utils import sign_in, sign_up, reset_password
from db_utils import add_medication, get_user_meds
from ai_bot import ask_ai_assistant
from vision_utils import extract_meds_from_image

st.set_page_config(page_title="MedRemind AI", layout="centered")

# Initialize Session State
if 'user' not in st.session_state:
    st.session_state.user = None

# --- AUTHENTICATION UI ---
if st.session_state.user is None:
    st.title("💊 MedRemind AI")
    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        pw = st.text_input("Password", type="password", key="login_pw")
        if st.button("Sign In"):
            sign_in(email, pw)
            st.rerun()

    with tab2:
        new_email = st.text_input("New Email")
        new_pw = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            sign_up(new_email, new_pw)
            st.success("Account created! You can now login.")

    with tab3:
        reset_email = st.text_input("Email for Reset")
        if st.button("Send Reset Link"):
            reset_password(reset_email)
            st.info("Reset link sent.")

# --- MAIN DASHBOARD ---
else:
    st.sidebar.write(f"Logged in as: {st.session_state.user.email}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.title("My Medications")

    # FEATURE: VISION AI UPLOAD
    with st.expander("📸 Smart Prescription Upload (AI)"):
        st.write("Upload a photo of your prescription to let AI identify your meds.")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Prescription", use_container_width=True)
            if st.button("🤖 Analyze with Gemini"):
                with st.spinner("AI is reading your prescription..."):
                    extracted_text = extract_meds_from_image(uploaded_file)
                    st.success("Analysis Complete!")
                    st.markdown(extracted_text)
                    st.caption("Copy these details into the manual form below to set reminders.")

    st.divider()

    # MANUAL ADD FORM
    with st.expander("➕ Add New Medication Manually"):
        name = st.text_input("Medicine Name")
        dose = st.text_input("Dosage (e.g. 500mg)")
        t = st.time_input("Reminder Time", datetime.time(9, 0))
        if st.button("Save Reminder"):
            add_medication(st.session_state.user.id, name, dose, t)
            st.success(f"Reminder for {name} saved!")
            st.rerun()

    # DISPLAY ACTIVE REMINDERS
    st.subheader("Today's Schedule")
    meds = get_user_meds(st.session_state.user.id)
    if meds:
        for m in meds:
            st.info(f"⏰ **{m['reminder_time']}** - {m['med_name']} ({m['dosage']})")
    else:
        st.write("No reminders set yet.")

    # AI CHAT ASSISTANT
    st.divider()
    st.subheader("🤖 AI Health Assistant")
    user_q = st.chat_input("Ask about your meds or side effects...")
    if user_q:
        with st.chat_message("user"):
            st.write(user_q)
        with st.chat_message("assistant"):
            response = ask_ai_assistant(user_q, meds)
            st.write(response)

    # SIMPLE ALERT TOASTS
    current_time = datetime.datetime.now().strftime("%H:%M")
    for m in meds:
        # Checking first 5 chars 'HH:MM'
        if m['reminder_time'][:5] == current_time:
            st.toast(f"🚨 Time to take your {m['med_name']}!", icon="💊")
