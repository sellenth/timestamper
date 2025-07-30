#!/usr/bin/env python3
"""Test YouTube video analysis with Gemini API"""

import os
import google.generativeai as genai
from pathlib import Path

# Load .env file
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Configure API
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Test with a simple model first
model = genai.GenerativeModel('gemini-2.5-flash')

youtube_url = "https://youtube.com/watch?v=EQynlpB6wCo"

print(f"Testing with URL: {youtube_url}")
print("Sending request...")

try:
    # Try the simple approach first
    response = model.generate_content([
        youtube_url,
        "What is happening at timestamp 00:30? Describe exactly what you see - people, objects, actions. Be very specific."
    ])
    print(f"\nResponse: {response.text}")
except Exception as e:
    print(f"\nError: {type(e).__name__}: {str(e)}")
    
    # Try with explicit content type
    try:
        print("\nTrying with explicit content structure...")
        response = model.generate_content(
            f"Analyze this YouTube video: {youtube_url}\n\nWhat is happening at timestamp 00:30?"
        )
        print(f"Response: {response.text}")
    except Exception as e2:
        print(f"Error 2: {type(e2).__name__}: {str(e2)}")