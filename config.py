import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    # This warning helps other developers know they are missing keys
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables.")