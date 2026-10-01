# Personal PDF RAG Chatbot 📄🤖

A complete, production-structured Retrieval-Augmented Generation (RAG) Chatbot application built with **Python, FastAPI, LangChain, ChromaDB, Google Gemini API**, and **React + Vite**.

Upload one or multiple PDF documents, process text chunks into high-dimensional vector embeddings stored in a persistent ChromaDB database, and interact with your documents using grounded AI conversational retrieval.

---

## 🌟 Features

- **Multi-PDF Document Support**: Upload multiple PDF files simultaneously.
- **Real RAG Pipeline**: Complete PDF text extraction (`PyPDFLoader`), chunking (`RecursiveCharacterTextSplitter`), Google vector embeddings, persistent vector store (`ChromaDB`), similarity retrieval, and LLM synthesis (`Gemini 1.5 Flash`).
- **Grounded & Anti-Hallucination Answers**: System prompts restrict Gemini to rely strictly on retrieved document context. When information is unavailable, it explicitly reports that it cannot find the answer.
- **Source Citations & Metadata**: Answers include clickable source citations specifying the exact document name, page number, and snippet text.
- **Selective Document Filtering**: Filter RAG search to specific uploaded PDFs or query across all indexed documents.
- **Document Management & Persistence**: View indexed document metadata (page count, chunk count, file size, ingestion status) and remove documents (deleting both physical files and ChromaDB vectors).
- **Session Chat Memory**: Maintains conversation ID across messages within a session.
- **Modern UI**: Dark-themed, glassmorphic React interface with upload drag & drop, file progress, auto-scrolling chat window, and Markdown code formatting.

---

## 🏗️ High-Level Architecture

```
                                 ┌──────────────────────┐
                                 │   React + Vite UI    │
                                 └──────────┬───────────┘
                                            │
                                 ┌──────────▼───────────┐
                                 │   FastAPI Backend    │
                                 └────┬────────────┬────┘
                                      │            │
             PDF Upload & Ingestion   │            │   Chat Question & RAG
          ┌───────────────────────────┘            └──────────────────────────┐
          │                                                                   │
┌─────────▼─────────┐                                              ┌──────────▼──────────┐
│   PyPDFLoader     │                                              │ RAGRetriever Search │
└─────────┬─────────┘                                              └──────────┬──────────┘
          │ (Pages)                                                           │
┌─────────▼─────────┐                                              ┌──────────▼──────────┐
│ Text Splitter     │                                              │ Top-K Chunks + Meta │
└─────────┬─────────┘                                              └──────────┬──────────┘
          │ (Chunks)                                                          │
┌─────────▼─────────┐                                              ┌──────────▼──────────┐
│ Google Embeddings │                                              │ Grounded Prompt     │
└─────────┬─────────┘                                              └──────────┬──────────┘
          │ (Vectors)                                                         │
┌─────────▼─────────┐                                              ┌──────────▼──────────┐
│ ChromaDB Store    │ ◄────────────────────────────────────────────┤ Gemini LLM          │
└───────────────────┘             Vector Search                    └──────────┬──────────┘
                                                                              │
                                                                   ┌──────────▼──────────┐
                                                                   │ Answer + Sources    │
                                                                   └─────────────────────┘
```

---

## 🔄 Complete RAG Flow

1. **PDF Upload**: User uploads PDFs via drag-and-drop or file picker.
2. **Text Extraction**: `PyPDFLoader` extracts text page-by-page while tracking `document_id`, `source`, and `page` numbers.
3. **Text Splitting**: `RecursiveCharacterTextSplitter` chunks documents using configurable `chunk_size` (1000) and `chunk_overlap` (200).
4. **Vector Embedding**: Text chunks are embedded using Google Gemini embeddings (`models/text-embedding-004`).
5. **ChromaDB Storage**: Embeddings and metadata are saved to persistent disk storage (`./data/chroma`).
6. **Retriever Search**: When a user asks a question, the question is embedded and Chroma performs a similarity search for top-K chunks.
7. **Prompt Assembly**: Retrieved text chunks with page headers are embedded into a strict grounded system prompt.
8. **Gemini Answer**: Gemini generates the final answer and attaches source citations.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, JavaScript, Modern CSS (Dark / Glassmorphism)
- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic
- **RAG Framework**: LangChain, `langchain-google-genai`, `langchain-chroma`, `langchain-community`
- **Vector Database**: ChromaDB (Persistent storage)
- **Embeddings & LLM**: Google Gemini API (`models/text-embedding-004` & `gemini-1.5-flash`)
- **PDF Processor**: PyPDF Loader (`pypdf`)

---

## 📁 Project Structure

```
Personal PDF RAG chatbot/
├── backend/
│   ├── main.py                  # FastAPI entry point & CORS configuration
│   ├── config.py                # Centralized environment configuration
│   ├── requirements.txt         # Python dependencies
│   ├── api/                     # REST API endpoints
│   │   ├── upload.py            # POST /api/documents/upload
│   │   ├── chat.py              # POST /api/chat
│   │   ├── documents.py         # GET / DELETE /api/documents
│   │   └── health.py            # GET /api/health
│   ├── rag/                     # Modular RAG components
│   │   ├── loader.py            # PDF loading & text extraction
│   │   ├── splitter.py          # Text chunking logic
│   │   ├── embeddings.py        # Google embedding model initialization
│   │   ├── vectorstore.py       # ChromaDB vector store manager
│   │   ├── retriever.py         # Top-K similarity search retriever
│   │   ├── prompt.py            # Grounded anti-hallucination prompt
│   │   └── chain.py             # End-to-end RAG execution chain
│   ├── models/                  # Pydantic schemas
│   │   └── schemas.py
│   └── utils/                   # Utilities & file management
│       ├── file_utils.py
│       ├── document_store.py
│       └── logging_config.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── services/api.js      # Centralized API service layer
│       ├── components/          # UI Components
│       │   ├── Header.jsx
│       │   ├── PDFUploader.jsx
│       │   ├── DocumentList.jsx
│       │   ├── ChatWindow.jsx
│       │   ├── ChatMessage.jsx
│       │   ├── SourceCard.jsx
│       │   └── LoadingIndicator.jsx
│       └── styles/global.css    # Custom styling
├── data/
│   ├── uploads/                 # Saved PDF files
│   └── chroma/                  # Persistent ChromaDB data
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory (or use `.env.example` as reference):

```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Model Configurations
EMBEDDING_MODEL=models/text-embedding-004
LLM_MODEL=gemini-1.5-flash

# Storage Paths
CHROMA_PERSIST_DIRECTORY=./data/chroma
UPLOAD_DIRECTORY=./data/uploads

# RAG Configurations
TOP_K=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

> **Security Note**: Never expose your `GEMINI_API_KEY` to the React frontend. The key is accessed exclusively on the FastAPI backend.

---

## 🚀 Setup & Execution Instructions

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### 2. Backend Setup
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Set your Google Gemini API key in `.env`.
4. Start the FastAPI server:
   ```bash
   python -m backend.main
   # or using uvicorn directly:
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The backend API will be available at: `http://localhost:8000` (Swagger docs at `http://localhost:8000/docs`).

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:3000` in your browser.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health status, document count, and API key readiness |
| `POST` | `/api/documents/upload` | Upload one or multiple PDFs and execute text extraction & indexing |
| `GET` | `/api/documents` | List all indexed documents with page, chunk, and status metadata |
| `DELETE` | `/api/documents/{document_id}` | Remove physical file and delete associated vectors from ChromaDB |
| `POST` | `/api/chat` | Submit question, retrieve context, and generate grounded answer |

---

## 🧪 Testing End-to-End RAG Flow

1. Start backend and frontend services.
2. Upload a sample PDF document (e.g., product manual, research paper, or Python documentation).
3. Observe status change: `uploaded` ➔ `processing` ➔ `✓ processed`.
4. Ask a specific question whose answer exists inside the document (e.g., *"What is the main topic covered in section 2?"*).
5. Verify that:
   - The LLM generates an accurate answer.
   - Source citations display document name and page number.
6. Ask a question completely unrelated to the PDF contents (e.g., *"Who won the 1998 World Cup?"*).
7. Verify that the chatbot responds with the anti-hallucination fallback: *"I couldn't find enough information about that in the uploaded documents."*
8. Delete the document and confirm vectors are deleted from ChromaDB.

---

## 🔮 Future Improvements Roadmap

- **Phase 2 (Advanced Document Processing)**: OCR integration (Tesseract/Unstructured) for scanned PDFs and table extraction.
- **Phase 3 (Hybrid & Advanced Retrieval)**: Maximal Marginal Relevance (MMR) search, BM25 hybrid search, and cross-encoder re-ranking.
- **Phase 4 (RAG Evaluation)**: Faithfulness and answer relevance scoring using Ragas evaluation framework.
- **Phase 5 (Multi-User & Persistence)**: User authentication, per-user document isolation, and PostgreSQL persistent chat history.
- **Phase 6 (Agentic RAG)**: Tool calling for automatic web search fallback when document context is insufficient.
