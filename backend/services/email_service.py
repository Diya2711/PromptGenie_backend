import smtplib
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email credentials
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Backend URL
BASE_URL = os.getenv(
    "BASE_URL",
    "https://promptgenie-backend.onrender.com"
)


def send_verification_email(email, token):

    print("🚀 EMAIL FUNCTION STARTED")

    # Debug environment variables
    print("📧 EMAIL_USER:", EMAIL_USER)
    print("🔑 EMAIL_PASS exists:", EMAIL_PASS is not None)

    # Verification link
    verification_link = (
        f"{BASE_URL}"
        f"/api/v1/auth/verify-email?token={token}"
    )

    try:

        print("🚀 Connecting to Gmail SMTP...")

        # Connect Gmail SMTP
        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        # Secure TLS connection
        server.starttls()

        print("🔐 Logging into Gmail...")

        # Login to Gmail
        server.login(
            EMAIL_USER,
            EMAIL_PASS
        )

        print("✅ Gmail login successful")

        # Email body
        body = f"""
Hello,

Welcome to PromptGenie 🚀

Please verify your email:

{verification_link}

This verification link expires in 1 hour.
"""

        # Create message
        msg = MIMEText(body)

        msg["Subject"] = "Verify Your PromptGenie Account"
        msg["From"] = EMAIL_USER
        msg["To"] = email

        print("📤 Sending email...")

        # Send email
        server.send_message(msg)

        print("✅ Email sent successfully")

        # Close server
        server.quit()

    except Exception as e:

        print("❌ EMAIL ERROR")
        print("❌", str(e))