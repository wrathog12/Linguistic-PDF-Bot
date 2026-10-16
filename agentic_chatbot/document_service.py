"""Document Service Module

Handles PDF document upload, text extraction, chunking, and embedding
into the Qdrant vector store for RAG-based retrieval.
"""

from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import pdfplumber
from rag_service import vectorstore
from config import CHUNK_SIZE, CHUNK_OVERLAP


async def process_document_upload(file: UploadFile, userid: str) -> dict:
    """Process an uploaded PDF: extract text, chunk it, and store embeddings.

    Args:
        file: The uploaded PDF file from the client.
        userid: Authenticated user's ID for document isolation.

    Returns:
        Dict with upload status, chunk count, and filename, or error details.
    """
    try:
        filename = file.filename
        if not filename.lower().endswith(".pdf"):
            return {"error": "Only PDF files are supported"}

        # Read PDF
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        # Chunk text
        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_text(text)

        # Batch create Document objects with metadata
        docs = [
            Document(page_content=chunk, metadata={"source": filename, "userid": userid})
            for chunk in chunks
        ]

        # ✅ Batch embed & insert
        vectorstore.add_documents(docs)

        return {"status": "uploaded", "chunks": len(docs), "file": filename}

    except Exception as e:
        return {"error": str(e)}
