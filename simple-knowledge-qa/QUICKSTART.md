# 🚀 Quick Start Guide

Get your minimal RAG system running in **5 minutes**!

---

## Prerequisites

- Python 3.9+ installed
- pip installed
- Terminal/Command Prompt

---

## Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd simple-knowledge-qa

# Install all required packages
pip install -r requirements.txt
```

**Note**: First time running will download the sentence-transformers model (~80MB). This is normal.

---

## Step 2: Start the Server (30 seconds)

```bash
# Start FastAPI server
python app.py
```

You should see:
```
Loading embedding model: all-MiniLM-L6-v2
Creating new FAISS index...
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Server is now running at: **http://localhost:8000**

---

## Step 3: Test It! (2 minutes)

### Option A: Using Browser

1. **Open Interactive Docs**
   - Go to: http://localhost:8000/docs
   - You'll see Swagger UI with all endpoints

2. **Check Status**
   - Click on `GET /status`
   - Click "Try it out"
   - Click "Execute"
   - Should show "healthy"

3. **Upload Document**
   - Click on `POST /upload`
   - Click "Try it out"
   - Choose file: `sample-documents/machine-learning.txt`
   - Click "Execute"

4. **Ask Question**
   - Click on `POST /ask`
   - Click "Try it out"
   - Enter: `{"question": "What is supervised learning?"}`
   - Click "Execute"
   - See the answer with source!

### Option B: Using curl

```bash
# Check status
curl http://localhost:8000/status

# Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@sample-documents/machine-learning.txt"

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is supervised learning?"}'

# List documents
curl http://localhost:8000/documents
```

---

## Expected Output

### Upload Response
```json
{
  "message": "Document uploaded successfully",
  "filename": "machine-learning.txt",
  "size": 2145
}
```

### Ask Response
```json
{
  "answer": "Supervised learning involves training a model on labeled data...",
  "source": "machine-learning.txt",
  "similarity": 0.8234
}
```

---

## Sample Questions to Try

After uploading `machine-learning.txt`:
- "What is supervised learning?"
- "Explain neural networks"
- "What is overfitting?"
- "What are the types of machine learning?"

After uploading `python-guide.txt`:
- "What are Python data types?"
- "How do you define functions in Python?"
- "What is a list comprehension?"

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt --upgrade
```

### Model Download Timeout
The first run downloads the embedding model. If it fails:
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Port Already in Use
```bash
# Use a different port
python -c "import uvicorn; from app import app; uvicorn.run(app, host='0.0.0.0', port=8001)"
```

### "No documents uploaded"
Make sure you uploaded a document first before asking questions!

---

## What Just Happened?

1. ✅ Server started
2. ✅ Sentence-transformers model loaded
3. ✅ FAISS index created
4. ✅ Document uploaded and chunked
5. ✅ Each chunk was embedded
6. ✅ Question was embedded
7. ✅ FAISS found most similar chunk
8. ✅ Result returned with source

**No LLM, no API keys, all local!**

---

## Next Steps

### For Development
- Upload more documents from `sample-documents/`
- Test different questions
- Check the `/status` endpoint
- Try `/rebuild` to reindex everything

### For Deployment
1. Create GitHub repository
2. Push your code
3. Follow the deployment guide in README.md
4. Deploy to Render (free tier available)

### For Submission
1. Update `ABOUTME.md` with your information
2. Test all features work
3. Deploy to Render
4. Submit your live URL and GitHub link

---

## File Structure

```
simple-knowledge-qa/
├── app.py              # FastAPI server (running)
├── rag.py              # Vector store logic
├── requirements.txt    # Dependencies
├── uploads/           # Your uploaded files (created after first upload)
├── vector_store/      # FAISS index (created after first upload)
└── sample-documents/  # Test files
```

---

## Common Commands

```bash
# Start server
python app.py

# Check status
curl http://localhost:8000/status

# Upload file
curl -X POST http://localhost:8000/upload -F "file=@yourfile.txt"

# Ask question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "your question"}'

# List documents
curl http://localhost:8000/documents

# Stop server
Ctrl + C
```

---

## Performance Notes

- **Model load**: ~3 seconds (first time only)
- **Upload**: ~1-2 seconds per document
- **Search**: <50ms per query
- **Embeddings**: ~100ms per chunk

---

## What Makes This Fast?

✅ **No external APIs** - Everything runs locally  
✅ **No LLM calls** - Pure vector search  
✅ **Efficient FAISS** - Optimized C++ library  
✅ **Small model** - all-MiniLM-L6-v2 (384 dim)  
✅ **Cached embeddings** - Stored in FAISS index  

---

## Ready for Production?

This is a **minimal viable product** suitable for:
- ✅ Small-scale deployments (<1000 documents)
- ✅ Personal knowledge bases
- ✅ Prototypes and demos
- ✅ Learning and experimentation

Not suitable for:
- ❌ Large-scale production (use Pinecone/Weaviate)
- ❌ Multi-user systems (add authentication)
- ❌ Complex queries (add LLM layer)

---

## Success! 🎉

If you got here, you have a working RAG system!

**Time spent**: ~5 minutes  
**Complexity**: Minimal  
**Cost**: $0  
**Understanding**: Complete  

Now you can:
1. Deploy it (see README.md)
2. Customize it (modify rag.py)
3. Extend it (add features to app.py)
4. Submit it (update ABOUTME.md)

Good luck! 🚀
