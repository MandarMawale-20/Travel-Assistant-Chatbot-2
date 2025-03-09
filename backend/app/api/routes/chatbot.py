from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.gemini_service import gemini_service
from app.api.routes.auth import get_current_user

router = APIRouter()

class ChatQuery(BaseModel):
    message: str
    location: Optional[str] = None
    preferences: Optional[str] = None
    budget: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

@router.post("/query", response_model=ChatResponse)
async def chat_query(query: ChatQuery, user = Depends(get_current_user)):
    try:
        if query.location:
            response = await gemini_service.get_travel_recommendations(
                query.location, 
                query.preferences, 
                query.budget
            )
        else:
            response = await gemini_service.answer_travel_query(query.message)
        
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying AI: {str(e)}")