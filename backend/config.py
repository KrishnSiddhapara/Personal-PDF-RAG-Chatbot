import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Root directory of the repository
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str = ""

    # Model Settings
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    LLM_MODEL: str = "gemini-2.5-flash"

    # Storage Paths
    CHROMA_PERSIST_DIRECTORY: str = str(BASE_DIR / "data" / "chroma")
    UPLOAD_DIRECTORY: str = str(BASE_DIR / "data" / "uploads")

    # RAG Settings
    TOP_K: int = 5
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # API Settings
    PROJECT_NAME: str = "Personal PDF RAG Chatbot"
    COLLECTION_NAME: str = "pdf_rag_collection"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
