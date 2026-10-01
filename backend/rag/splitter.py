from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.config import settings
from backend.utils.logging_config import logger

def split_documents(
    documents: List[Document],
    chunk_size: int = settings.CHUNK_SIZE,
    chunk_overlap: int = settings.CHUNK_OVERLAP
) -> List[Document]:
    """
    Splits LangChain Document objects into smaller chunks using RecursiveCharacterTextSplitter,
    preserving document metadata.
    """
    logger.info(f"Splitting {len(documents)} document pages with chunk_size={chunk_size}, overlap={chunk_overlap}")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"Generated {len(chunks)} text chunks.")
    return chunks
