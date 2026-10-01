import os
from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from backend.config import settings
from backend.models.schemas import DocumentUploadResponse, DocumentInfo, DocumentStatus
from backend.utils.file_utils import sanitize_filename, generate_document_id, validate_pdf_file
from backend.utils.document_store import document_store
from backend.rag.loader import load_pdf, PDFProcessingError
from backend.rag.splitter import split_documents
from backend.rag.vectorstore import vector_store_manager
from backend.utils.logging_config import logger

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Handles PDF document uploads:
    1. Validates files
    2. Saves PDF safely
    3. Extracts pages
    4. Chunks text
    5. Stores embeddings in ChromaDB
    """
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files provided.")

    processed_docs: List[DocumentInfo] = []

    for file in files:
        original_filename = file.filename or "file.pdf"
        sanitized_name = sanitize_filename(original_filename)
        
        try:
            content = await file.read()
            is_valid, err_msg = validate_pdf_file(original_filename, content)
            
            if not is_valid:
                doc_info = DocumentInfo(
                    document_id="invalid_" + str(hash(original_filename)),
                    filename=sanitized_name,
                    status=DocumentStatus.FAILED,
                    upload_time=datetime.now().isoformat(),
                    file_size=len(content),
                    error_message=err_msg
                )
                processed_docs.append(doc_info)
                continue

            # Compute unique document ID
            doc_id = generate_document_id(content, original_filename)
            upload_path = os.path.join(settings.UPLOAD_DIRECTORY, f"{doc_id}_{sanitized_name}")
            
            # Save file to disk
            with open(upload_path, "wb") as f:
                f.write(content)

            # Record uploaded status
            doc_info = DocumentInfo(
                document_id=doc_id,
                filename=sanitized_name,
                status=DocumentStatus.PROCESSING,
                upload_time=datetime.now().isoformat(),
                file_size=len(content)
            )
            document_store.add_or_update(doc_info)

            # Process RAG ingestion
            try:
                pages = load_pdf(upload_path, doc_id, sanitized_name)
                chunks = split_documents(pages)
                chunk_count = vector_store_manager.add_documents(chunks, doc_id)

                document_store.update_status(
                    document_id=doc_id,
                    status=DocumentStatus.PROCESSED,
                    page_count=len(pages),
                    chunk_count=chunk_count
                )
                
                updated_doc = document_store.get(doc_id)
                if updated_doc:
                    processed_docs.append(updated_doc)

            except Exception as proc_err:
                logger.error(f"Failed RAG processing for {sanitized_name}: {str(proc_err)}")
                document_store.update_status(
                    document_id=doc_id,
                    status=DocumentStatus.FAILED,
                    error_message=str(proc_err)
                )
                updated_doc = document_store.get(doc_id)
                if updated_doc:
                    processed_docs.append(updated_doc)

        except Exception as e:
            logger.error(f"Unexpected error uploading {file.filename}: {str(e)}")
            failed_info = DocumentInfo(
                document_id="err_" + str(hash(original_filename)),
                filename=sanitized_name,
                status=DocumentStatus.FAILED,
                upload_time=datetime.now().isoformat(),
                error_message=str(e)
            )
            processed_docs.append(failed_info)

    has_successful = any(d.status == DocumentStatus.PROCESSED for d in processed_docs)
    
    return DocumentUploadResponse(
        success=has_successful,
        documents=processed_docs,
        message="Documents uploaded and processed." if has_successful else "Document processing failed."
    )
