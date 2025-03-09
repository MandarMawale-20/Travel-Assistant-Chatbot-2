from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import httpx
from app.core.config import settings
from app.api.routes.auth import get_current_user

router = APIRouter()

class PlaceDetailsRequest(BaseModel):
    place_id: str
    fields: Optional[str] = None

class PlaceSearchRequest(BaseModel):
    query: str
    location: Optional[str] = None  # "lat,lng" format
    radius: Optional[int] = 10000

@router.post("/details")
async def place_details(request: PlaceDetailsRequest, user = Depends(get_current_user)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/details/json",
                params={
                    "place_id": request.place_id,
                    "fields": request.fields or "name,rating,formatted_address,geometry,photo,type,url",
                    "key": settings.GOOGLE_MAPS_API_KEY
                }
            )
            data = response.json()
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting place details: {str(e)}")

@router.post("/search")
async def place_search(request: PlaceSearchRequest, user = Depends(get_current_user)):
    try:
        params = {
            "query": request.query,
            "key": settings.GOOGLE_MAPS_API_KEY
        }
        
        if request.location:
            params.update({
                "location": request.location,
                "radius": request.radius
            })
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://maps.googleapis.com/maps/api/place/textsearch/json",
                params=params
            )
            data = response.json()
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching places: {str(e)}")