from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class PromptRequest(BaseModel):
    raw_idea: str

class PromptResponse(BaseModel):
    id: Optional[str] = None
    category: str
    score: int
    prompts: Dict[str, str]  # Basic, Advanced, Developer

class HistoryEntry(BaseModel):
    id: Optional[str] = None
    raw_idea: str
    category: str
    score: int
    prompts: Dict[str, str]
    created_at: datetime

