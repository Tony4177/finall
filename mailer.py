import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_medicine_notification(receiver_email, med_name, dosage, time_str):
    # Email credentials from Render Env Variables
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASS")

    # Set up the email content
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = receiver_email
    em['Subject'] = f"⏰ Time for your Medicine: {med_name}"
    
    body = f"Hello,\n\nIt is time to take your {med_name} ({dosage}) scheduled for {time_str}."
    em.set_content(body)

    # Create SSL context and send
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(em)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
