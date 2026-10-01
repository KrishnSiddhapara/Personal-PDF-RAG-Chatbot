from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"

class DocumentInfo(BaseModel):
    document_id: str = Field(..., description="Unique document hash or identifier")
    filename: str = Field(..., description="Sanitized original file name")
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED, description="Ingestion status")
    upload_time: str = Field(..., description="ISO timestamp of upload")
    page_count: int = Field(default=0, description="Total pages extracted from PDF")
    chunk_count: int = Field(default=0, description="Total text chunks generated")
    file_size: int = Field(default=0, description="File size in bytes")
    error_message: Optional[str] = Field(default=None, description="Error details if status is failed")

class DocumentUploadResponse(BaseModel):
    success: bool
    documents: List[DocumentInfo]
    message: str

class ChatMessageRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User's query")
    document_ids: Optional[List[str]] = Field(default=None, description="Optional list of document IDs to restrict search")
    conversation_id: Optional[str] = Field(default=None, description="Session conversation ID")

class SourceCitation(BaseModel):
    document_id: str
    filename: str
    page: Optional[int] = None
    snippet: str = ""

class ChatMessageResponse(BaseModel):
    answer: str
    sources: List[SourceCitation]
    conversation_id: str
    timestamp: str

class DocumentDeleteResponse(BaseModel):
    success: bool
    document_id: str
    message: str

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    document_count: int
    has_api_key: bool
