import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import ChatMessageRequest, ChatMessageResponse
from backend.rag.chain import rag_chain
from backend.utils.logging_config import logger

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("", response_model=ChatMessageResponse)
async def chat(request: ChatMessageRequest):
    """
    RAG Chat endpoint:
    Processes question, retrieves relevant vector chunks, invokes Gemini LLM,
    and returns answer with citations.
    """
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty."
        )

    conversation_id = request.conversation_id or str(uuid.uuid4())
    logger.info(f"Chat request received [conv_id={conversation_id}]: '{request.question}'")

    try:
        result = rag_chain.answer_question(
            question=request.question.strip(),
            document_ids=request.document_ids
        )

        return ChatMessageResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat()
        )

    except ValueError as ve:
        logger.error(f"Configuration or validation error during chat: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Error handling chat request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the answer. Please try again."
        )
