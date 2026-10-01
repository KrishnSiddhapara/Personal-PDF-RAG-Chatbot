import os
import glob
from typing import List
from fastapi import APIRouter, HTTPException, status
from backend.config import settings
from backend.models.schemas import DocumentInfo, DocumentDeleteResponse
from backend.utils.document_store import document_store
from backend.rag.vectorstore import vector_store_manager
from backend.utils.logging_config import logger

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.get("", response_model=List[DocumentInfo])
async def list_documents():
    """Returns list of all uploaded documents and their ingestion statuses."""
    docs = document_store.get_all()
    logger.info(f"Listing {len(docs)} registered documents.")
    return docs

@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
async def delete_document(document_id: str):
    """
    Deletes a document:
    1. Removes associated physical PDF file from disk
    2. Deletes vectors from ChromaDB
    3. Removes document entry from metadata store
    """
    logger.info(f"Received deletion request for document_id: {document_id}")
    
    doc = document_store.get(document_id)
    if not doc:
        # Check if vectors exist even if not in store
        vector_store_manager.delete_document(document_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{document_id}' not found."
        )

    # 1. Delete file from disk
    pattern = os.path.join(settings.UPLOAD_DIRECTORY, f"{document_id}_*")
    matching_files = glob.glob(pattern)
    for file_path in matching_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted physical file: {file_path}")
        except Exception as file_err:
            logger.warning(f"Could not delete physical file {file_path}: {str(file_err)}")

    # 2. Delete vectors from ChromaDB
    vector_store_manager.delete_document(document_id)

    # 3. Remove metadata entry
    document_store.remove(document_id)

    return DocumentDeleteResponse(
        success=True,
        document_id=document_id,
        message=f"Document '{doc.filename}' successfully deleted."
    )
