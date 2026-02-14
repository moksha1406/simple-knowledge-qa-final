# Simple Knowledge Q&A - RAG with Google Gemini

A minimal RAG (Retrieval-Augmented Generation) system using FAISS, sentence transformers, and **Google Gemini** for natural language answers.

## 🎯 Features

- ✅ Upload `.txt` documents
- ✅ FAISS vector store with sentence-transformers embeddings
- ✅ **Google Gemini (gemini-pro) for natural language answers**
- ✅ Retrieve relevant document chunks by similarity
- ✅ Return AI-generated answer + source + similarity score
- ✅ Status endpoint showing system health
- ✅ List all uploaded documents
- ✅ **FREE to use** (Gemini has generous free tier)

## 📁 Project Structure

```
simple-knowledge-qa/
├── app.py              # FastAPI application
├── rag.py              # FAISS vector store logic
├── requirements.txt    # Python dependencies
├── uploads/           # Uploaded documents (created on first upload)
└── vector_store/      # FAISS index (created on first upload)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip
- **Google Gemini API key** (FREE - get at https://makersuite.google.com/app/apikey)

### Installation

```bash
# Clone or download the project
cd simple-knowledge-qa

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your Gemini API key to .env file
# GEMINI_API_KEY=your_key_here
```

### Run Locally

```bash
# Start the server
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

**See GEMINI_SETUP.md for detailed setup instructions!**

## 📖 API Documentation

### 1. Upload Document

```bash
POST /upload

curl -X POST http://localhost:8000/upload \
  -F "file=@document.txt"
```

**Response:**
```json
{
  "message": "Document uploaded successfully",
  "filename": "document.txt",
  "size": 1234
}
```

### 2. Ask Question

```bash
POST /ask

curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

**Response:**
```json
{
  "answer": "Machine learning is a subset of AI that...",
  "source": "ai-basics.txt",
  "similarity": 0.8234
}
```

### 3. List Documents

```bash
GET /documents

curl http://localhost:8000/documents
```

**Response:**
```json
{
  "documents": [
    {
      "filename": "ai-basics.txt",
      "size_bytes": 5432
    }
  ],
  "count": 1
}
```

### 4. System Status

```bash
GET /status

curl http://localhost:8000/status
```

**Response:**
```json
{
  "status": "healthy",
  "backend": "running",
  "vector_store": {
    "exists": true,
    "total_chunks": 45,
    "total_documents": 3,
    "dimension": 384
  },
  "uploads_directory": {
    "exists": true,
    "file_count": 3
  }
}
```

### 5. Delete Document

```bash
DELETE /documents/{filename}

curl -X DELETE http://localhost:8000/documents/document.txt
```

### 6. Rebuild Index

```bash
POST /rebuild

curl -X POST http://localhost:8000/rebuild
```

Rebuilds FAISS index from all files in `uploads/` directory.

## 🧪 Testing

### Using curl

```bash
# 1. Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@test.txt"

# 2. Check status
curl http://localhost:8000/status

# 3. Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "your question here"}'

# 4. List documents
curl http://localhost:8000/documents
```

### Using Python

```python
import requests

# Upload
with open('document.txt', 'rb') as f:
    response = requests.post('http://localhost:8000/upload', files={'file': f})
    print(response.json())

# Ask question
response = requests.post('http://localhost:8000/ask', 
    json={'question': 'What is AI?'})
print(response.json())
```

### Interactive API Docs

Open in browser: `http://localhost:8000/docs`

FastAPI provides interactive Swagger UI for testing all endpoints.

## 🚀 Deploy to Render

### Step 1: Prepare Repository

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/simple-knowledge-qa.git
git push -u origin main
```

### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `simple-knowledge-qa`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free

### Step 3: Deploy

- Click "Create Web Service"
- Wait 3-5 minutes for deployment
- Your API will be live at: `https://your-app.onrender.com`

### Step 4: Test Deployed API

```bash
# Replace with your Render URL
curl https://your-app.onrender.com/status
```

### Important Notes for Render

1. **Free tier sleeps after 15 minutes** of inactivity
   - First request after sleep takes ~30 seconds
   - Subsequent requests are fast

2. **Uploads are ephemeral** on free tier
   - Files uploaded will be deleted when app restarts
   - Use paid tier ($7/month) for persistent storage
   - Or rebuild index on startup from a cloud storage bucket

3. **Vector store persistence**
   - Vector store is saved to disk but lost on restart (free tier)
   - Consider using paid tier with persistent disk

## 🛠️ How It Works

### Architecture

```
1. User uploads .txt file
   ↓
2. Text is split into chunks (500 words each)
   ↓
3. Each chunk is embedded using sentence-transformers
   ↓
4. Embeddings are stored in FAISS index
   ↓
5. When user asks a question:
   - Question is embedded
   - FAISS finds most similar chunk
   - Return chunk content + source + similarity
```

### Key Components

**rag.py**
- `SimpleRAG` class handles all vector operations
- Uses `all-MiniLM-L6-v2` for embeddings (384 dimensions)
- FAISS `IndexFlatL2` for L2 distance search
- Chunks text into 500-word segments

**app.py**
- FastAPI server with 6 endpoints
- File upload handling
- Error handling and validation
- CORS enabled for browser access

## ✅ What's Implemented

- ✅ Document upload and storage
- ✅ FAISS vector indexing
- ✅ Similarity-based retrieval
- ✅ Source attribution
- ✅ Status monitoring
- ✅ Document listing
- ✅ Document deletion
- ✅ Index rebuilding

## ❌ What's NOT Implemented

- ❌ LLM-based answer generation
- ❌ OpenAI API integration
- ❌ Database (SQLite/PostgreSQL)
- ❌ User authentication
- ❌ Frontend UI
- ❌ Conversation history
- ❌ Multi-document summarization

## 🔧 Configuration

### Chunking

Edit `rag.py`:
```python
def _chunk_text(self, text: str, chunk_size: int = 500):
    # Change chunk_size to adjust chunk length
```

### Embedding Model

Edit `rag.py`:
```python
def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
    # Options: 
    # - "all-MiniLM-L6-v2" (fast, 384 dim)
    # - "all-mpnet-base-v2" (better quality, 768 dim)
```

### Number of Results

Edit `app.py`:
```python
results = rag.search(question, top_k=1)
# Increase top_k to return more results
```

## 📊 Performance

- **Upload**: ~1-2 seconds per document
- **Indexing**: ~100ms per chunk
- **Search**: <50ms for typical queries
- **Model loading**: ~2-3 seconds on startup

## 🐛 Troubleshooting

### Model download fails
```bash
# Pre-download the model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### FAISS installation issues
```bash
# Use conda instead
conda install -c pytorch faiss-cpu
```

### Encoding errors
- Ensure all uploaded files are UTF-8 encoded
- Use `iconv` to convert: `iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt`

## 📝 Sample Questions

After uploading documents about AI:
- "What is machine learning?"
- "Explain neural networks"
- "What are the types of AI?"

The system will return the most relevant chunk from your documents.

## 🔒 Security Notes

- No API keys required ✅
- File upload limited to `.txt` only
- No external API calls
- All processing happens locally

## 📄 License

MIT License - Use freely for your projects.

## 🙋 FAQ

**Q: Why no LLM?**
A: This is a minimal retrieval system. Adding LLM would require API keys and costs.

**Q: Can I use PDF files?**
A: No, only `.txt` files. You can convert PDFs to text first.

**Q: How accurate is the retrieval?**
A: Depends on your documents. Works best with clear, well-written content.

**Q: Can I use a different embedding model?**
A: Yes, edit `model_name` in `rag.py`. See sentence-transformers documentation.

**Q: How do I persist uploads on Render?**
A: Use Render's paid tier with persistent disk, or store files in S3/cloud storage.

---

Built for simplicity and ease of deployment. No unnecessary complexity.
