import os
import resend

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Resend API Key
resend.api_key = os.getenv("RESEND_API_KEY")

# Backend URL
BASE_URL = os.getenv(
    "BASE_URL",
    "https://promptgenie-backend.onrender.com"
)


def send_verification_email(email, token):

    try:

        verification_link = (
            f"{BASE_URL}"
            f"/api/v1/auth/verify-email?token={token}"
        )

        html_content = f"""
        <h2>Welcome to PromptGenie 🚀</h2>

        <p>Please verify your email:</p>

        <a href="{verification_link}">
            Verify Email
        </a>

        <p>This link expires in 1 hour.</p>
        """

        response = resend.Emails.send({

            "from": "onboarding@resend.dev",

            "to": email,

            "subject": "Verify Your PromptGenie Account",

            "html": html_content

        })

        print("✅ Verification email sent")
        print(response)

    except Exception as e:

        print("❌ Email sending failed")
        print(str(e))