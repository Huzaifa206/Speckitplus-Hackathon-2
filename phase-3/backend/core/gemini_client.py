"""
Google Gemini Client Configuration using OpenAI Compatible API
"""
import os
from openai import OpenAI
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class GeminiConfig:
    """Configuration for Google Gemini API"""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Clean the API key of any surrounding quotes if present
        self.api_key = self.api_key.strip().strip("'\"")

        self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

        # Default model to use
        self.default_model = "gemini-2.0-flash"  # Updated to a more recent model

    def get_client(self):
        """Return configured OpenAI client for Gemini"""
        return self.client

    def get_default_model(self):
        """Return the default model name"""
        return self.default_model


# Global instance
gemini_config = GeminiConfig()


def get_gemini_client():
    """Get the configured Gemini client"""
    return gemini_config.get_client()


def get_gemini_model():
    """Get the default model name"""
    return gemini_config.get_default_model()


class ToolCall(BaseModel):
    """Represents a tool call from the AI"""
    name: str
    arguments: Dict[str, Any]


class GeminiResponse(BaseModel):
    """Structure for Gemini API responses"""
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    finish_reason: str