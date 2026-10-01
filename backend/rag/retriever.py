from typing import List, Optional, Dict, Any
from langchain_core.documents import Document
from backend.config import settings
from backend.rag.vectorstore import vector_store_manager
from backend.models.schemas import SourceCitation
from backend.utils.logging_config import logger

class RAGRetriever:
    """Retriever component that fetches relevant text chunks and extracts citations."""

    def retrieve(
        self,
        query: str,
        top_k: int = settings.TOP_K,
        filter_doc_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Executes similarity search on ChromaDB.
        Returns retrieved Documents and extracted SourceCitations.
        """
        logger.info(f"Retrieving top {top_k} chunks for query: '{query}'")
        
        search_results = vector_store_manager.similarity_search(
            query=query,
            top_k=top_k,
            filter_doc_ids=filter_doc_ids
        )
        
        retrieved_docs: List[Document] = []
        sources: List[SourceCitation] = []
        seen_citations = set()

        for doc, score in search_results:
            retrieved_docs.append(doc)
            meta = doc.metadata or {}
            
            doc_id = meta.get("document_id", "unknown")
            filename = meta.get("source", "unknown.pdf")
            page = meta.get("page")
            
            citation_key = (doc_id, filename, page)
            if citation_key not in seen_citations:
                seen_citations.add(citation_key)
                snippet = doc.page_content[:150].strip().replace("\n", " ") + "..."
                sources.append(
                    SourceCitation(
                        document_id=doc_id,
                        filename=filename,
                        page=page,
                        snippet=snippet
                    )
                )

        logger.info(f"Retrieved {len(retrieved_docs)} chunks from {len(sources)} distinct page sources.")
        return {
            "documents": retrieved_docs,
            "sources": sources
        }

rag_retriever = RAGRetriever()
