import os
import resend

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Resend API Key
resend.api_key = os.getenv("RESEND_API_KEY")

# ✅ Backend Base URL
BASE_URL = os.getenv(
    "BASE_URL",
    "https://promptgenie-backend.onrender.com"
)


def send_verification_email(email, token):

    try:

        print("🚀 Sending verification email...")

        # ✅ Verification link
        verification_link = (
            f"{BASE_URL}"
            f"/api/v1/auth/verify-email?token={token}"
        )

        # ✅ HTML Email
        html_content = f"""
        <div style="font-family: Arial; padding: 20px;">

            <h2>
                Welcome to PromptGenie 🚀
            </h2>

            <p>
                Thank you for registering.
            </p>

            <p>
                Please verify your email address
                by clicking the button below:
            </p>

            <a
                href="{verification_link}"
                style="
                    background:#6366F1;
                    color:white;
                    padding:12px 20px;
                    text-decoration:none;
                    border-radius:8px;
                    display:inline-block;
                    margin-top:10px;
                "
            >
                Verify Email
            </a>

            <p style="margin-top:20px;">
                This verification link
                will expire in 1 hour.
            </p>

            <p>
                PromptGenie Team
            </p>

        </div>
        """

        # ✅ Send Email using Resend
        response = resend.Emails.send({

            # ⚠️ KEEP THIS until domain is verified
            "from": "onboarding@resend.dev",

            "to": email,

            "subject": "Verify Your PromptGenie Account",

            "html": html_content

        })

        print("✅ Verification email sent successfully")
        print(response)

    except Exception as e:

        print("❌ Email sending failed")
        print(str(e))