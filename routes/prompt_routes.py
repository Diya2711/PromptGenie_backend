from fastapi import APIRouter, HTTPException, Depends
from models.schemas import PromptRequest, PromptResponse
from services.prompt_service import generate_optimized_prompts
from database.db import history_collection
from routes.auth_routes import get_current_user, get_optional_user
from typing import Optional
import datetime

router = APIRouter()

@router.post("/generate", response_model=PromptResponse)
def generate_prompt(request: PromptRequest, user_id: Optional[str] = Depends(get_optional_user)):
    if not request.raw_idea.strip():
        raise HTTPException(status_code=400, detail="Raw idea cannot be empty")
    
    result = generate_optimized_prompts(request.raw_idea)
    
    # Save to MongoDB
    try:
        doc = {
            "raw_idea": request.raw_idea,
            "category": result.get("category"),
            "score": result.get("score"),
            "prompts": result.get("prompts"),
            "created_at": datetime.datetime.utcnow()
        }
        if user_id:
            doc["user_id"] = user_id
        inserted = history_collection.insert_one(doc)
        result["id"] = str(inserted.inserted_id)
    except Exception as e:
        print(f"Failed to save to database: {e}")
        
    return result

@router.get("/history", response_model=list[dict])
def get_history(user_id: str = Depends(get_current_user)):
    docs = list(history_collection.find({"user_id": user_id}).sort("created_at", -1).limit(50))
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
    return docs
