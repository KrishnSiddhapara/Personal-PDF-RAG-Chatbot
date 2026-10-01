import json
import os
from typing import Dict, List, Optional
from pathlib import Path
from backend.config import settings
from backend.models.schemas import DocumentInfo, DocumentStatus
from backend.utils.logging_config import logger

METADATA_FILE = Path(settings.UPLOAD_DIRECTORY).parent / "documents_metadata.json"

class DocumentStore:
    """Manages persistence of document metadata."""
    
    def __init__(self):
        self._store: Dict[str, DocumentInfo] = {}
        self._load()

    def _load(self):
        if METADATA_FILE.exists():
            try:
                with open(METADATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for doc_id, doc_dict in data.items():
                        self._store[doc_id] = DocumentInfo(**doc_dict)
                logger.info(f"Loaded {len(self._store)} documents from metadata store.")
            except Exception as e:
                logger.error(f"Failed to load document metadata file: {str(e)}")

    def _save(self):
        try:
            with open(METADATA_FILE, "w", encoding="utf-8") as f:
                data = {doc_id: doc.model_dump() for doc_id, doc in self._store.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save document metadata file: {str(e)}")

    def get_all(self) -> List[DocumentInfo]:
        return list(self._store.values())

    def get(self, document_id: str) -> Optional[DocumentInfo]:
        return self._store.get(document_id)

    def add_or_update(self, doc_info: DocumentInfo):
        self._store[doc_info.document_id] = doc_info
        self._save()

    def update_status(
        self,
        document_id: str,
        status: DocumentStatus,
        page_count: int = 0,
        chunk_count: int = 0,
        error_message: Optional[str] = None
    ):
        if document_id in self._store:
            doc = self._store[document_id]
            doc.status = status
            if page_count > 0:
                doc.page_count = page_count
            if chunk_count > 0:
                doc.chunk_count = chunk_count
            doc.error_message = error_message
            self._save()

    def remove(self, document_id: str) -> Optional[DocumentInfo]:
        if document_id in self._store:
            doc = self._store.pop(document_id)
            self._save()
            return doc
        return None

document_store = DocumentStore()
