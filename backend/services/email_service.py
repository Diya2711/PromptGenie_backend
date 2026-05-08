import smtplib
import ssl
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

BASE_URL = os.getenv(
    "BASE_URL",
    "https://promptgenie-backend.onrender.com"
)


def send_verification_email(email, token):

    print("🚀 EMAIL FUNCTION STARTED")
    print("📧 EMAIL_USER:", EMAIL_USER)
    print("🔑 EMAIL_PASS exists:", EMAIL_PASS is not None)

    verification_link = (
        f"{BASE_URL}"
        f"/api/v1/auth/verify-email?token={token}"
    )

    body = f"""
Hello,

Welcome to PromptGenie 🚀

Verify your email below:

{verification_link}

Thank you,
PromptGenie Team
"""

    msg = MIMEText(body)

    msg["Subject"] = "Verify Your PromptGenie Account"
    msg["From"] = EMAIL_USER
    msg["To"] = email

    try:

        print("🚀 Connecting with SSL...")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
         "smtp.gmail.com",
          465,
          context=context,
          timeout=30
          ) as server:
            print("🔐 Logging in...")

            server.login(
                EMAIL_USER,
                EMAIL_PASS
            )
            print("✅ Gmail login successful")
            print("📤 Sending email...")

            server.send_message(msg)

            print("✅ Email sent successfully")

    except Exception as e:

        print("❌ EMAIL ERROR")
        print(str(e))