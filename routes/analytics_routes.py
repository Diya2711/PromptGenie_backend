from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database.db import analytics_collection, history_collection, users_collection
from routes.auth_routes import get_optional_user, get_current_user
import datetime

router = APIRouter()

class FeedbackRequest(BaseModel):
    history_id: str
    is_helpful: bool

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest, user_id: str = Depends(get_optional_user)):
    feedback_doc = {
        "history_id": request.history_id,
        "is_helpful": request.is_helpful,
        "created_at": datetime.datetime.utcnow()
    }
    if user_id:
        feedback_doc["user_id"] = user_id
        
    analytics_collection.insert_one(feedback_doc)
    return {"message": "Feedback submitted successfully"}

@router.get("/stats")
def get_analytics_stats():
    total_prompts = history_collection.count_documents({})
    total_users = users_collection.count_documents({})
    
    # Simple category aggregation
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    categories = list(history_collection.aggregate(pipeline))
    
    # Calculate average score
    score_pipeline = [
        {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
    ]
    score_result = list(history_collection.aggregate(score_pipeline))
    avg_score = score_result[0]["avg_score"] if score_result else 0
    
    total_feedback = analytics_collection.count_documents({})
    positive_feedback = analytics_collection.count_documents({"is_helpful": True})
    satisfaction_rate = (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
    
    return {
        "total_prompts_generated": total_prompts,
        "total_users": total_users,
        "average_prompt_score": round(avg_score, 1),
        "satisfaction_rate_percentage": round(satisfaction_rate, 1),
        "top_categories": [{"category": c["_id"], "count": c["count"]} for c in categories]
    }
