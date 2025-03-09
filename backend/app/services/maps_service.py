import httpx
from app.core.config import settings

class MapsService:
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://maps.googleapis.com/maps/api"
        
    async def geocode_address(self, address):
        """Convert address to coordinates"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/geocode/json",
                params={
                    "address": address,
                    "key": self.api_key
                }
            )
            data = response.json()
            return data
            
    async def get_nearby_places(self, location, place_type, radius=1500):
        """Get nearby places of interest"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/place/nearbysearch/json",
                params={
                    "location": location,  # "lat,lng" format
                    "radius": radius,
                    "type": place_type,
                    "key": self.api_key
                }
            )
            data = response.json()
            return data
            
    async def get_directions(self, origin, destination, mode="driving"):
        """Get directions between two points"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/directions/json",
                params={
                    "origin": origin,  # "lat,lng" or address
                    "destination": destination,  # "lat,lng" or address
                    "mode": mode,
                    "key": self.api_key
                }
            )
            data = response.json()
            return data

maps_service = MapsService()