from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.api.routes import auth, chatbot, maps, places
from app.core.config import settings
from app.middleware.error_handler import validation_exception_handler, general_exception_handler
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if not settings.DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(chatbot.router, prefix=f"{settings.API_V1_STR}/chatbot", tags=["Chatbot"])
app.include_router(maps.router, prefix=f"{settings.API_V1_STR}/maps", tags=["Maps"])
app.include_router(places.router, prefix=f"{settings.API_V1_STR}/places", tags=["Places"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}", "version": "1.0.0", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}