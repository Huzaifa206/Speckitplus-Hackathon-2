"""
Configuration and environment variable validation for Phase 3
"""
import os
from typing import Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

    # Gemini API settings
    GEMINI_API_KEY: str

    # Application settings
    APP_NAME: str = "Todo App - Phase 3"
    API_V1_STR: str = "/api"
    DEBUG: bool = False

    # Validation
    @validator("GEMINI_API_KEY")
    def gemini_api_key_must_not_be_empty(cls, v):
        if not v or v == "your_google_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY must be set with a valid API key")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings():
    """Get application settings with validation"""
    return Settings()


# Validate settings on import
settings = get_settings()

# Additional validation for required environment variables
def validate_environment():
    """Validate that all required environment variables are set"""
    errors = []

    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_google_gemini_api_key_here":
        errors.append("GEMINI_API_KEY is not set properly")

    if not settings.DATABASE_URL:
        errors.append("DATABASE_URL is not set")

    if errors:
        raise ValueError(f"Environment validation failed: {'; '.join(errors)}")


# Run validation
validate_environment()