import smtplib
from email.mime.text import MIMEText
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

def send_verification_email(email, token):
    link = f"{BASE_URL}/api/v1/auth/verify-email?token={token}"

    subject = "Verify Your Email"
    body = f"""
Hello,

Click below to verify your email:
{link}

This link expires in 1 hour.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = email

    try:
        # ✅ CORRECT METHOD
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print("✅ Verification email sent")

    except Exception as e:
        print("❌ Email sending failed:", str(e))