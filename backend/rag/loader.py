from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from backend.utils.logging_config import logger

class PDFProcessingError(Exception):
    """Custom exception raised when PDF loading or extraction fails."""
    pass

def load_pdf(file_path: str, document_id: str, original_filename: str) -> List[Document]:
    """
    Loads a PDF file and extracts text page by page into LangChain Document objects.
    Attaches standardized metadata to each document page.
    """
    try:
        logger.info(f"Loading PDF from path: {file_path} for doc_id: {document_id}")
        loader = PyPDFLoader(file_path)
        raw_documents = loader.load()

        if not raw_documents:
            raise PDFProcessingError("No readable pages found in PDF.")

        processed_docs = []
        for i, doc in enumerate(raw_documents):
            # PyPDFLoader usually uses 0-indexed page in metadata
            raw_page = doc.metadata.get("page", i)
            page_num = raw_page + 1 if isinstance(raw_page, int) else i + 1

            page_text = doc.page_content.strip()
            if not page_text:
                continue

            metadata = {
                "document_id": document_id,
                "source": original_filename,
                "page": int(page_num)
            }
            processed_docs.append(Document(page_content=page_text, metadata=metadata))

        if not processed_docs:
            raise PDFProcessingError("PDF does not contain any extractable text (it might be scanned or image-only).")

        logger.info(f"Successfully loaded {len(processed_docs)} text-bearing pages from {original_filename}")
        return processed_docs

    except Exception as e:
        logger.error(f"Error loading PDF {original_filename}: {str(e)}")
        if isinstance(e, PDFProcessingError):
            raise e
        raise PDFProcessingError(f"Failed to process PDF file: {str(e)}")
