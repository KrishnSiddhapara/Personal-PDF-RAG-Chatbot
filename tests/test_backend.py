import os
import sys
import unittest
from fastapi.testclient import TestClient

# Ensure root workspace directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app
from backend.config import settings

class TestRAGBackend(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.uploaded_doc_ids = []

    def test_1_health_check(self):
        """Test health endpoint."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("has_api_key", data)
        print("\n[TEST OK] Health Check Endpoint Response:", data)

    def test_2_upload_documents(self):
        """Test uploading PDF files and RAG vector indexing."""
        pdf1_path = "scratch/test_pdfs/rag_architecture.pdf"
        pdf2_path = "scratch/test_pdfs/company_policy.pdf"

        self.assertTrue(os.path.exists(pdf1_path), "Sample PDF 1 does not exist.")
        self.assertTrue(os.path.exists(pdf2_path), "Sample PDF 2 does not exist.")

        with open(pdf1_path, "rb") as f1, open(pdf2_path, "rb") as f2:
            files = [
                ("files", ("rag_architecture.pdf", f1, "application/pdf")),
                ("files", ("company_policy.pdf", f2, "application/pdf"))
            ]
            response = self.client.post("/api/documents/upload", files=files)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(len(data["documents"]), 2)

        for doc in data["documents"]:
            print(f"[TEST OK] Uploaded Doc ID: {doc['document_id']} | File: {doc['filename']} | Status: {doc['status']} | Pages: {doc['page_count']} | Chunks: {doc['chunk_count']}")
            self.assertIn(doc["status"], ["processed", "uploaded", "processing"])
            if doc["status"] == "processed":
                self.assertGreater(doc["page_count"], 0)
                self.assertGreater(doc["chunk_count"], 0)
                self.__class__.uploaded_doc_ids.append(doc["document_id"])

    def test_3_list_documents(self):
        """Test GET /api/documents."""
        response = self.client.get("/api/documents")
        self.assertEqual(response.status_code, 200)
        docs = response.json()
        self.assertGreaterEqual(len(docs), 2)
        print(f"[TEST OK] Listed {len(docs)} documents in registry.")

    def test_4_chat_rag_pipeline(self):
        """Test chat endpoint retrieval & response generation."""
        if not settings.GEMINI_API_KEY:
            print("\n[SKIP] Skipping live Gemini API chat test because GEMINI_API_KEY is not configured.")
            return

        # Query 1: Information present in rag_architecture.pdf
        payload1 = {
            "question": "What are the steps in Retrieval-Augmented Generation?",
            "document_ids": [],
            "conversation_id": "test_conv_1"
        }
        res1 = self.client.post("/api/chat", json=payload1)
        self.assertEqual(res1.status_code, 200)
        data1 = res1.json()
        print("\n[TEST OK] Chat Question 1 Answer:\n", data1["answer"])
        print("[TEST OK] Sources:", data1["sources"])
        self.assertTrue(len(data1["answer"]) > 0)

        # Query 2: Information present in company_policy.pdf
        payload2 = {
            "question": "What is the meal expense limit per day?",
            "document_ids": [],
            "conversation_id": "test_conv_1"
        }
        res2 = self.client.post("/api/chat", json=payload2)
        self.assertEqual(res2.status_code, 200)
        data2 = res2.json()
        print("\n[TEST OK] Chat Question 2 Answer:\n", data2["answer"])
        print("[TEST OK] Sources:", data2["sources"])

        # Query 3: Unrelated question for anti-hallucination check
        payload3 = {
            "question": "Who won the 1994 FIFA World Cup final in soccer?",
            "document_ids": [],
            "conversation_id": "test_conv_1"
        }
        res3 = self.client.post("/api/chat", json=payload3)
        self.assertEqual(res3.status_code, 200)
        data3 = res3.json()
        print("\n[TEST OK] Unrelated Question Fallback Answer:\n", data3["answer"])
        self.assertIn("couldn't find", data3["answer"].lower())

    def test_5_delete_document(self):
        """Test DELETE /api/documents/{document_id}."""
        if not self.__class__.uploaded_doc_ids:
            return
            
        target_doc_id = self.__class__.uploaded_doc_ids[0]
        response = self.client.delete(f"/api/documents/{target_doc_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        print(f"\n[TEST OK] Deleted Document ID: {target_doc_id}")

        # Verify removal from list
        list_res = self.client.get("/api/documents")
        remaining_ids = [d["document_id"] for d in list_res.json()]
        self.assertNotIn(target_doc_id, remaining_ids)

if __name__ == "__main__":
    unittest.main()
