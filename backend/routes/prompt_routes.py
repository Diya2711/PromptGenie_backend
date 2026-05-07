from fastapi import APIRouter, HTTPException, Depends
from models.schemas import PromptRequest, PromptResponse
from services.prompt_service import generate_optimized_prompts
from routes.auth_routes import get_current_user, oauth2_scheme
from database.db import history_collection, users_collection
from bson import ObjectId
import datetime

router = APIRouter()


# 🚀 GENERATE PROMPT (WITH JWT AUTH)
@router.post("/generate", response_model=PromptResponse)
def generate_prompt(
    request: PromptRequest,
    current_user: str = Depends(get_current_user)
):

    if not request.raw_idea.strip():
        raise HTTPException(
            status_code=400,
            detail="Raw idea cannot be empty"
        )

    # ✅ Generate prompts
    result = generate_optimized_prompts(request.raw_idea)

    # ✅ Save history in MongoDB
    try:
        doc = {
            "user_id": ObjectId(current_user),
            "raw_idea": request.raw_idea,
            "category": result.get("category"),
            "score": result.get("score"),
            "prompts": result.get("prompts"),
            "created_at": datetime.datetime.utcnow()
        }

        inserted = history_collection.insert_one(doc)

        result["id"] = str(inserted.inserted_id)

    except Exception as e:
        print(f"❌ Failed to save history: {e}")

    return result


# 🚀 GET HISTORY (WITH JWT AUTH)
@router.get("/history")
def get_history(current_user: str = Depends(get_current_user)):
    
    try:
        user_id = ObjectId(current_user)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    docs = list(
        history_collection
        .find({"user_id": user_id})
        .sort("created_at", -1)
        .limit(50)
    )

    for doc in docs:
        doc["_id"] = str(doc["_id"])
        doc["user_id"] = str(doc["user_id"])

    return docs