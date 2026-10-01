import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.utils.logging_config import logger
from backend.api import upload, chat, documents, health

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Production-Structured RAG Chatbot API using LangChain, ChromaDB, and Gemini LLM",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(documents.router)
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing Personal PDF RAG Chatbot Backend...")
    logger.info(f"Upload Directory: {settings.UPLOAD_DIRECTORY}")
    logger.info(f"Chroma Directory: {settings.CHROMA_PERSIST_DIRECTORY}")
    logger.info(f"LLM Model: {settings.LLM_MODEL}")
    logger.info(f"Embedding Model: {settings.EMBEDDING_MODEL}")
    if not settings.GEMINI_API_KEY:
        logger.warning("ATTENTION: GEMINI_API_KEY is not set in environment or backend/.env!")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
