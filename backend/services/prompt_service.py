import os
import json

from dotenv import load_dotenv
import google.generativeai as genai

from ml.classifier import (
    predict_category,
    get_prompt_score
)

load_dotenv()

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )
else:
    model = None


def generate_optimized_prompts(raw_idea: str) -> dict:

    category = predict_category(raw_idea)
    score = get_prompt_score(raw_idea)

    # =========================
    # GEMINI AI GENERATION
    # =========================
    if model:
        try:

            system_prompt = f"""
You are a Prompt Engineering expert.

User idea:
"{raw_idea}"

Return ONLY valid JSON in this exact format:

{{
  "Basic": "...",
  "Advanced": "...",
  "Developer": "..."
}}

Rules:
- Basic = simple prompt
- Advanced = detailed product-level prompt
- Developer = technical architecture prompt
- No markdown
- No explanation
- Only JSON
"""

            response = model.generate_content(
                system_prompt
            )

            text = response.text.strip()

            # Remove markdown formatting if Gemini adds it
            if text.startswith("```"):
                text = (
                    text.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            prompts = json.loads(text)

            return {
                "category": category,
                "score": score + 15,
                "prompts": {
                    "Basic": prompts.get(
                        "Basic",
                        "Basic prompt generation failed"
                    ),

                    "Advanced": prompts.get(
                        "Advanced",
                        "Advanced prompt generation failed"
                    ),

                    "Developer": prompts.get(
                        "Developer",
                        "Developer prompt generation failed"
                    )
                }
            }

        except Exception as e:
            print("Gemini Error:", str(e))

    # =========================
    # FALLBACK PROMPTS
    # =========================

    basic = f"""
Act as a professional in {category}.

Help me build:
"{raw_idea}"

Provide:
1. Core idea
2. Features
3. Users
4. Benefits
"""

    advanced = f"""
Act as a Product Manager.

Convert this into a complete roadmap:
"{raw_idea}"

Include:
- MVP
- Features
- Monetization
- Scaling strategy
- UI/UX suggestions
"""

    developer = f"""
Act as a Senior Software Engineer.

Design architecture for:
"{raw_idea}"

Include:
1. Tech stack
2. Backend APIs
3. Database schema
4. Authentication
5. Deployment
6. Scalability
"""

    return {
        "category": category,
        "score": score,
        "prompts": {
            "Basic": basic,
            "Advanced": advanced,
            "Developer": developer
        }
    }