import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# API Keys
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Agent Configuration
STRATEGIST_MODEL = os.environ.get("STRATEGIST_MODEL", "gemini-1.5-flash-001")
QUERY_MODEL = os.environ.get("QUERY_MODEL", "gemini-1.5-flash-001")
KNOWLEDGE_BASE_DIR = os.environ.get("KNOWLEDGE_BASE_DIR", "knowledge_base")