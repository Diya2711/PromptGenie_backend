import smtplib
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email credentials
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Backend base URL
BASE_URL = os.getenv(
    "BASE_URL",
    "https://promptgenie-backend.onrender.com"
)


def send_verification_email(email, token):

    # Verification link
    verification_link = (
        f"{BASE_URL}"
        f"/api/v1/auth/verify-email?token={token}"
    )

    # Email subject
    subject = "Verify Your PromptGenie Account"

    # Email body
    body = f"""
Hello,

Welcome to PromptGenie 🚀

Please verify your email by clicking the link below:

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
        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            # Secure connection
            server.starttls()

            # Login to Gmail
            server.login(
                EMAIL_USER,
                EMAIL_PASS
            )

            # Send email
            server.send_message(msg)

        print("✅ Verification email sent successfully")

    except Exception as e:
        print(
            "❌ Email sending failed:",
            str(e)
        )