import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# API Keys
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Agent Configuration
MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.0-flash")
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.8"))
KNOWLEDGE_BASE_DIR = os.environ.get("KNOWLEDGE_BASE_DIR", "knowledge_base")