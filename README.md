Simple Knowledge Q&A (RAG with FAISS + Gemini)

A minimal Retrieval-Augmented Generation (RAG) API built using FastAPI, FAISS, sentence-transformers, and Google Gemini.

The system allows users to upload .txt documents, retrieves relevant chunks using vector similarity search, and generates answers using Gemini based on retrieved context.

Tech Stack

Python 3.9+

FastAPI

FAISS (IndexFlatL2)

sentence-transformers (all-MiniLM-L6-v2)

Google Gemini API

Features

Upload .txt documents

Automatic text chunking (500 words)

Vector embeddings (384 dimensions)

Similarity search using FAISS

Gemini-based answer generation

Source attribution with similarity score

Document listing and deletion

Index rebuild support

Health/status endpoint

Project Structure
simple-knowledge-qa/
├── app.py
├── rag.py
├── requirements.txt
├── uploads/
└── vector_store/

How It Works

Uploaded documents are split into 500-word chunks.

Each chunk is converted into a vector embedding using all-MiniLM-L6-v2.

Embeddings are stored in a FAISS IndexFlatL2.

When a user asks a question:

The question is embedded.

FAISS retrieves the most similar chunk.

The retrieved context is sent to Gemini.

The API returns the generated answer along with the source file and similarity score.

Setup
1. Install Dependencies
pip install -r requirements.txt

2. Configure Environment Variables

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

Design Decisions

FAISS IndexFlatL2 used for simplicity and fast similarity search.

all-MiniLM-L6-v2 chosen for lightweight embeddings with good performance.

Chunk size fixed at 500 words to balance retrieval accuracy and context size.

Single vector store architecture (not multi-tenant).

Limitations

Supports only .txt files

No authentication

No conversation memory

No persistent storage on free hosting tiers

Single-document retrieval per query (top_k = 1)

Deployment

The application can be deployed on:

Render

Railway

Any VPS running Python

Docker-based environments

Start command:

uvicorn app:app --host 0.0.0.0 --port 8000

Future Improvements

PDF and DOCX support

Persistent vector storage (e.g., pgvector)

Multi-chunk retrieval (top_k > 1 with context merging)

Streaming responses

Basic frontend interface

Authentication layer
