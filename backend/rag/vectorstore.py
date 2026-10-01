from typing import List, Optional, Tuple, Set
from langchain_core.documents import Document
from langchain_chroma import Chroma
from backend.config import settings
from backend.rag.embeddings import get_embedding_model
from backend.utils.logging_config import logger

class VectorStoreManager:
    """Manages persistent Chroma vector store operations."""
    
    def __init__(self):
        self._vectorstore: Optional[Chroma] = None

    def get_vectorstore(self) -> Chroma:
        """Lazily initializes and returns the persistent Chroma vector store."""
        if self._vectorstore is None:
            embedding_model = get_embedding_model()
            logger.info(f"Connecting to persistent Chroma store at: {settings.CHROMA_PERSIST_DIRECTORY}")
            self._vectorstore = Chroma(
                collection_name=settings.COLLECTION_NAME,
                embedding_function=embedding_model,
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY
            )
        return self._vectorstore

    def add_documents(self, documents: List[Document], document_id: str) -> int:
        """
        Adds document chunks to Chroma. If document_id already exists in vectorstore,
        removes existing chunks first to prevent duplicate entries.
        """
        vs = self.get_vectorstore()
        
        # Remove pre-existing chunks for this document_id if any exist
        self.delete_document(document_id)
        
        if not documents:
            return 0
            
        logger.info(f"Inserting {len(documents)} chunks for document_id: {document_id}")
        # Generate clean chunk IDs
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(documents))]
        vs.add_documents(documents=documents, ids=chunk_ids)
        logger.info(f"Successfully indexed document_id: {document_id}")
        return len(documents)

    def delete_document(self, document_id: str) -> bool:
        """Deletes all chunks belonging to document_id from the vector store."""
        vs = self.get_vectorstore()
        try:
            # Query Chroma for IDs matching the metadata document_id
            existing = vs.get(where={"document_id": document_id})
            if existing and existing.get("ids"):
                ids_to_delete = existing["ids"]
                logger.info(f"Deleting {len(ids_to_delete)} vector store chunks for document_id: {document_id}")
                vs.delete(ids=ids_to_delete)
                return True
            logger.info(f"No existing vectors found for document_id: {document_id}")
            return False
        except Exception as e:
            logger.warning(f"Error during deletion of doc_id {document_id} from vector store: {str(e)}")
            return False

    def similarity_search(
        self,
        query: str,
        top_k: int = settings.TOP_K,
        filter_doc_ids: Optional[List[str]] = None
    ) -> List[Tuple[Document, float]]:
        """
        Searches vector store for chunks matching the query.
        Supports optional filtering by specific document IDs.
        """
        vs = self.get_vectorstore()
        
        # Construct Chroma metadata filter
        filter_kwargs = None
        if filter_doc_ids and len(filter_doc_ids) > 0:
            if len(filter_doc_ids) == 1:
                filter_kwargs = {"document_id": filter_doc_ids[0]}
            else:
                filter_kwargs = {"document_id": {"$in": filter_doc_ids}}
                
        logger.info(f"Performing similarity search. Query: '{query}', top_k: {top_k}, filter: {filter_kwargs}")
        results = vs.similarity_search_with_score(query=query, k=top_k, filter=filter_kwargs)
        return results

    def get_indexed_document_ids(self) -> Set[str]:
        """Returns the set of unique document IDs currently stored in Chroma."""
        try:
            vs = self.get_vectorstore()
            data = vs.get(include=["metadatas"])
            metadatas = data.get("metadatas", [])
            doc_ids = {meta["document_id"] for meta in metadatas if meta and "document_id" in meta}
            return doc_ids
        except Exception as e:
            logger.error(f"Failed to fetch indexed document IDs: {str(e)}")
            return set()

# Singleton instance
vector_store_manager = VectorStoreManager()
