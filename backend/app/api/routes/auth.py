from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.firebase_service import firebase_service
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class UserProfile(BaseModel):
    uid: str
    email: str
    name: str = None
    photo_url: str = None

@router.post("/verify-token", response_model=UserProfile)
async def verify_token(token: str):
    decoded_token = await firebase_service.verify_token(token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user data from the token
    uid = decoded_token.get("uid")
    email = decoded_token.get("email", "")
    name = decoded_token.get("name", "")
    photo_url = decoded_token.get("picture", "")
    
    return UserProfile(uid=uid, email=email, name=name, photo_url=photo_url)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_token = await firebase_service.verify_token(token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return decoded_token