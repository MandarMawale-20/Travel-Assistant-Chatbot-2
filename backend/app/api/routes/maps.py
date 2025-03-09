from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.maps_service import maps_service
from app.api.routes.auth import get_current_user

router = APIRouter()

class GeocodeRequest(BaseModel):
    address: str

class NearbyPlacesRequest(BaseModel):
    location: str  # "lat,lng" format
    place_type: str
    radius: Optional[int] = 1500

class DirectionsRequest(BaseModel):
    origin: str
    destination: str
    mode: Optional[str] = "driving"

@router.post("/geocode")
async def geocode(request: GeocodeRequest, user = Depends(get_current_user)):
    try:
        result = await maps_service.geocode_address(request.address)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error geocoding address: {str(e)}")

@router.post("/nearby-places")
async def nearby_places(request: NearbyPlacesRequest, user = Depends(get_current_user)):
    try:
        result = await maps_service.get_nearby_places(
            request.location,
            request.place_type,
            request.radius
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding nearby places: {str(e)}")

@router.post("/directions")
async def directions(request: DirectionsRequest, user = Depends(get_current_user)):
    try:
        result = await maps_service.get_directions(
            request.origin,
            request.destination,
            request.mode
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting directions: {str(e)}")