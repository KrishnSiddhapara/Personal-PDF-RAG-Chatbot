from langchain_core.embeddings import Embeddings, FakeEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.config import settings
from backend.utils.logging_config import logger

def get_embedding_model() -> Embeddings:
    """
    Returns the LangChain embedding model.
    Uses GoogleGenerativeAIEmbeddings if GEMINI_API_KEY is configured;
    otherwise falls back to local embeddings for vector store indexing.
    """
    if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
        logger.info(f"Initializing Google embeddings model: {settings.EMBEDDING_MODEL}")
        return GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GEMINI_API_KEY
        )
    else:
        logger.warning(
            "GEMINI_API_KEY is not configured in backend/.env. "
            "Using local fallback embeddings for ChromaDB vector indexing."
        )
        return FakeEmbeddings(size=768)
