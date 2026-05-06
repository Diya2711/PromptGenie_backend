import os
import json
from dotenv import load_dotenv
from google import genai
from ml.classifier import predict_category, get_prompt_score

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Create Gemini client ONLY if key exists
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def generate_optimized_prompts(raw_idea: str) -> dict:
    category = predict_category(raw_idea)
    score = get_prompt_score(raw_idea)

    # ✅ Use Gemini if API key exists
    if client:
        try:
            system_prompt = f"""
You are a Prompt Engineering expert.

User idea:
"{raw_idea}"

Return ONLY valid JSON with this format:
{{
  "Basic": "...",
  "Advanced": "...",
  "Developer": "..."
}}

Rules:
- Basic = simple, high-level prompt
- Advanced = product-level detailed prompt
- Developer = technical architecture prompt
- No extra text, only JSON
"""

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=system_prompt
            )

            text = response.text.strip()

            # ✅ Clean markdown if exists
            if text.startswith("```"):
                text = text.replace("```json", "").replace("```", "").strip()

            prompts = json.loads(text)

            return {
                "category": category,
                "score": score + 15,  # AI boost
                "prompts": {
                    "Basic": prompts.get("Basic", "Error generating Basic prompt"),
                    "Advanced": prompts.get("Advanced", "Error generating Advanced prompt"),
                    "Developer": prompts.get("Developer", "Error generating Developer prompt")
                }
            }

        except Exception as e:
            print(f"Gemini API Error: {e}")
            # fallback below

    # ✅ Fallback (no API or error)
    basic = f"""Act as a seasoned professional in {category}.
I want to build: "{raw_idea}"

Provide:
1. Core features
2. Target users
3. Challenges & solutions
"""

    advanced = f"""You are a Product Manager.

Convert this idea into a roadmap:
"{raw_idea}"

Include:
- Summary
- MVP
- Future features
- Strategy
"""

    developer = f"""Act as a Senior Engineer.

Design system for:
"{raw_idea}"

Include:
1. Tech stack
2. Database design
3. APIs
4. Scalability
5. Implementation steps
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