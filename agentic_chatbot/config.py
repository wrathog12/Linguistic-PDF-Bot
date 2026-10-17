"""Configuration Module

Centralizes all environment variables, model settings, and application
constants. Validates that critical API keys are present at startup.
"""

from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger("voicebot")

# ==================== API Keys ====================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MURF_API_KEY = os.environ.get("MURF_API_KEY")

# ==================== Model Configuration ====================
EMBEDDING_MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"
EMBEDDING_SIZE = 768
ASR_MODEL = "whisper-large-v3-turbo"

# ==================== Text Processing ====================
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ==================== Qdrant Configuration ====================
QDRANT_HOST = os.environ.get("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.environ.get("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.environ.get("QDRANT_COLLECTION", "documents")

# ==================== CORS Configuration ====================
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

# ==================== Startup Validation ====================
_required_keys = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "MURF_API_KEY": MURF_API_KEY,
}

for key_name, key_value in _required_keys.items():
    if not key_value:
        logger.warning(f"⚠️  Missing environment variable: {key_name}")
