# Simple Knowledge Q&A - RAG with Google Gemini

A minimal Retrieval-Augmented Generation (RAG) API built using FastAPI, FAISS, sentence-transformers, and Google Gemini.

The system allows users to upload .txt documents, retrieves relevant chunks using vector similarity search, and generates answers using Gemini based on retrieved context.

## 🎯 Features

Upload .txt documents
Automatic text chunking (500 words)
Vector embeddings (384 dimensions)
Similarity search using FAISS
Gemini-based answer generation
Source attribution with similarity score
Document listing and deletion
Index rebuild support
Health/status endpoint

## 📁 Project Structure

```
simple-knowledge-qa/
├── app.py              # FastAPI application
├── rag.py              # FAISS vector store logic
├── requirements.txt    # Python dependencies
├── uploads/           # Uploaded documents (created on first upload)
└── vector_store/      # FAISS index (created on first upload)
```

## Tech Stack

Python 3.9+
FastAPI
FAISS (IndexFlatL2)
sentence-transformers (all-MiniLM-L6-v2)
Google Gemini API

## How It Works

Uploaded documents are split into 500-word chunks.
Each chunk is converted into a vector embedding using all-MiniLM-L6-v2.
Embeddings are stored in a FAISS IndexFlatL2.
When a user asks a question:
The question is embedded.
FAISS retrieves the most similar chunk.
The retrieved context is sent to Gemini.
The API returns the generated answer along with the source file and similarity score.

## Setup
-1. Install Dependencies
pip install -r requirements.txt

-2. Configure Environment Variables
Create a .env file:

GEMINI_API_KEY=your_api_key_here

3. Run the Application
uvicorn app:app --host 0.0.0.0 --port 8000

API base URL:
http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

API Endpoints
Upload Document
POST /upload

Ask Question
POST /ask


Request body:

{
  "question": "What is machine learning?"
}


Response:

{
  "answer": "...",
  "source": "document.txt",
  "similarity": 0.82
}

List Documents
GET /documents

Delete Document
DELETE /documents/{filename}

Rebuild Index
POST /rebuild

System Status
GET /status


## ✅ What's Implemented

- ✅ Document upload and storage
- ✅ FAISS vector indexing
- ✅ Similarity-based retrieval
- ✅ Source attribution
- ✅ Status monitoring
- ✅ Document listing
- ✅ Document deletion
- ✅ Index rebuilding

## 📊 Performance

- **Upload**: ~1-2 seconds per document
- **Indexing**: ~100ms per chunk
- **Search**: <50ms for typical queries
- **Model loading**: ~2-3 seconds on startup

## Limitations
Supports only .txt files
No authentication
No conversation memory
No persistent storage on free hosting tiers
Single-document retrieval per query (top_k = 1)

Built for simplicity and ease of deployment. No unnecessary complexity.
