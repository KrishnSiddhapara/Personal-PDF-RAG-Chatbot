from typing import List, Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from backend.config import settings
from backend.rag.retriever import rag_retriever
from backend.rag.prompt import get_rag_prompt
from backend.models.schemas import SourceCitation
from backend.utils.logging_config import logger

class RAGChain:
    """Orchestrates document retrieval and LLM answer generation."""

    def __init__(self):
        self._llm = None

    def get_llm(self) -> Optional[ChatGoogleGenerativeAI]:
        """Lazily initializes the Gemini Chat Model if API key is provided."""
        if not settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY.strip():
            logger.warning("GEMINI_API_KEY is not configured.")
            return None

        if self._llm is None:
            logger.info(f"Initializing ChatGoogleGenerativeAI with model: {settings.LLM_MODEL}")
            self._llm = ChatGoogleGenerativeAI(
                model=settings.LLM_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.2,
                max_output_tokens=2048
            )
        return self._llm

    def _format_context(self, docs: List[Document]) -> str:
        """Formats retrieved documents into a clean context string for the prompt."""
        formatted_chunks = []
        for doc in docs:
            meta = doc.metadata or {}
            source = meta.get("source", "Unknown Document")
            page = meta.get("page", "Unknown Page")
            header = f"[Document: {source}, Page: {page}]"
            content = doc.page_content.strip()
            formatted_chunks.append(f"{header}\n{content}")
        return "\n\n---\n\n".join(formatted_chunks)

    def answer_question(
        self,
        question: str,
        document_ids: Optional[List[str]] = None,
        top_k: int = settings.TOP_K
    ) -> Dict[str, Any]:
        """
        Executes full RAG workflow:
        1. Retrieval of top-k chunks from ChromaDB
        2. Context formatting
        3. Prompt construction & Gemini LLM call
        4. Structured answer & citation response
        """
        # 1. Retrieve relevant chunks
        retrieval_res = rag_retriever.retrieve(
            query=question,
            top_k=top_k,
            filter_doc_ids=document_ids
        )
        
        docs: List[Document] = retrieval_res["documents"]
        sources: List[SourceCitation] = retrieval_res["sources"]

        # 2. Check if any context was retrieved
        if not docs:
            logger.info("No matching chunks retrieved for question.")
            return {
                "answer": "I couldn't find enough information about that in the uploaded documents.",
                "sources": []
            }

        # 3. Check LLM availability
        llm = self.get_llm()
        if llm is None:
            context_summary = "\n\n".join([f"• {doc.page_content[:200]}..." for doc in docs[:3]])
            fallback_answer = (
                "⚠️ **GEMINI_API_KEY is missing from backend/.env.**\n\n"
                "The RAG retrieval pipeline successfully found relevant text chunks in ChromaDB. "
                "Please add your `GEMINI_API_KEY` to `backend/.env` to enable Gemini AI answer synthesis.\n\n"
                "**Retrieved Document Snippets:**\n" + context_summary
            )
            return {
                "answer": fallback_answer,
                "sources": sources
            }

        # 4. Format context & build prompt
        context_str = self._format_context(docs)
        prompt_template = get_rag_prompt()
        prompt_value = prompt_template.format_messages(
            context=context_str,
            question=question
        )

        # 5. Invoke LLM
        try:
            logger.info("Sending prompt to Gemini LLM...")
            response = llm.invoke(prompt_value)
            answer_text = response.content
            if isinstance(answer_text, list):
                answer_text = "".join([str(b) for b in answer_text])
            return {
                "answer": str(answer_text).strip(),
                "sources": sources
            }
        except Exception as e:
            logger.error(f"Error calling Gemini LLM: {str(e)}")
            raise e

rag_chain = RAGChain()
