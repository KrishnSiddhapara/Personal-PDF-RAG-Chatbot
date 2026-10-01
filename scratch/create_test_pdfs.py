import os

def create_simple_pdf(filepath: str, text_lines: list):
    content_stream = "BT /F1 12 Tf 50 750 Td 16 TL\n"
    for line in text_lines:
        clean_line = line.replace("(", "\\(").replace(")", "\\)")
        content_stream += f"({clean_line}) ' \n"
    content_stream += "ET"

    stream_bytes = content_stream.encode('latin-1')
    stream_len = len(stream_bytes)

    pdf_template = (
        f"%PDF-1.4\n"
        f"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        f"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        f"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
        f"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        f"5 0 obj\n<< /Length {stream_len} >>\nstream\n"
        f"{content_stream}\n"
        f"endstream\nendobj\n"
        f"xref\n0 6\n"
        f"0000000000 65535 f \n"
        f"0000000009 00000 n \n"
        f"0000000058 00000 n \n"
        f"00000000115 00000 n \n"
        f"00000000244 00000 n \n"
        f"00000000315 00000 n \n"
        f"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        f"startxref\n400\n%%EOF"
    )

    with open(filepath, "wb") as f:
        f.write(pdf_template.encode('latin-1'))

if __name__ == "__main__":
    os.makedirs("scratch/test_pdfs", exist_ok=True)
    
    pdf1_text = [
        "Retrieval-Augmented Generation RAG Overview",
        "RAG combines document retrieval with large language models.",
        "Step 1: Text from PDF documents is extracted and split into chunks.",
        "Step 2: Chunks are converted into vector embeddings.",
        "Step 3: Embeddings are stored in ChromaDB vector database.",
        "Step 4: User asks a query, retriever fetches top 5 chunks.",
        "Step 5: Google Gemini LLM answers using the retrieved context."
    ]
    create_simple_pdf("scratch/test_pdfs/rag_architecture.pdf", pdf1_text)

    pdf2_text = [
        "Company Expense and Travel Policy 2026",
        "Employees can claim up to 50 dollars per day for meal expenses.",
        "All receipts above 20 dollars must be submitted within 30 days.",
        "Flight bookings must be made at least 14 days in advance in economy class.",
        "Remote equipment allowance is 500 dollars one-time upon joining."
    ]
    create_simple_pdf("scratch/test_pdfs/company_policy.pdf", pdf2_text)

    print("Test PDFs generated in scratch/test_pdfs/")
