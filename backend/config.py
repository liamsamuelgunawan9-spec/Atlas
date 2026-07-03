import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Atlas"
VERSION = "0.1.0"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Model fallback order (highest quality first)
MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

# Request timeout (seconds)
REQUEST_TIMEOUT = 60