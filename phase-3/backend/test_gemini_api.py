#!/usr/bin/env python3
"""
Simple test script to verify Gemini API connectivity
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment")
    exit(1)

print("Testing Gemini API connection...")

# Clean the API key of any surrounding quotes if present
api_key = api_key.strip().strip("'\"")

# Create the client
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

try:
    # Test the API connection with a simple request
    print("Making test request to Gemini API...")
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        max_tokens=50
    )

    print("\n✅ API Connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    print("\nThe API key is working correctly.")

except Exception as e:
    print(f"\n❌ API Error: {e}")
    print("\nThis could be due to:")
    print("- Incorrect API key")
    print("- API not enabled in Google Cloud Console")
    print("- Billing not set up")
    print("- Rate limits exceeded")
    print("- Network connectivity issues")