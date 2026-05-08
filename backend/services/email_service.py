import smtplib
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load .env variables
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

    # Debug logs
    print("📧 EMAIL_USER:", EMAIL_USER)
    print("🔑 EMAIL_PASS exists:", EMAIL_PASS is not None)

    # Verification link
    verification_link = (
        f"{BASE_URL}"
        f"/api/v1/auth/verify-email?token={token}"
    )

    # Subject
    subject = "Verify Your PromptGenie Account"

    # Email content
    body = f"""
Hello,

Welcome to PromptGenie 🚀

Please click the link below to verify your email:

{verification_link}

This verification link will expire in 1 hour.

Thank you,
PromptGenie Team
"""

    # Create email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = email

    try:
        print("🚀 Connecting to Gmail SMTP...")

        # Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)

        # Start secure TLS
        server.starttls()

        print("🔐 Logging into Gmail...")

        # Login
        server.login(
            EMAIL_USER,
            EMAIL_PASS
        )

        print("📤 Sending verification email...")

        # Send email
        server.send_message(msg)

        # Close connection
        server.quit()

        print("✅ Verification email sent successfully")

    except Exception as e:

        print("❌ Email sending failed")
        print("❌ Error:", str(e))