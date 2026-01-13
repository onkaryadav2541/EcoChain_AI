import os
from dotenv import load_dotenv

load_dotenv()

# We are now looking for the Google Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY found in environment variables")