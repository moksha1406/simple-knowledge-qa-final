
"""
Simple Knowledge Q&A FastAPI Application
RAG with Google Gemini for natural language answers.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List
from rag import SimpleRAG
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()



app = FastAPI(title="Simple Knowledge Q&A")

# CORS middleware for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag = SimpleRAG()

# Initialize Google Gemini
# Initialize Google Gemini (New SDK)
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_client = None

if gemini_api_key:
    try:
        gemini_client = genai.Client(api_key=gemini_api_key)

        print("✅ Google Gemini initialized successfully")
    except Exception as e:
        print(f"⚠️ Gemini initialization failed: {e}")
else:
    print("⚠️ GEMINI_API_KEY not set - will use retrieval-only mode")


# Request models
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Simple Knowledge Q&A API",
        "version": "1.0",
        "endpoints": {
            "POST /upload": "Upload a .txt document",
            "GET /documents": "List all uploaded documents",
            "POST /ask": "Ask a question (retrieval only)",
            "GET /status": "System status",
            "POST /rebuild": "Rebuild vector index"
        }
    }

@app.get("/status")
def status():
    """
    Get system status.
    Shows backend health, vector store status, Gemini API status, and document count.
    """
    stats = rag.get_stats()
    
    # Check if uploads directory exists
    uploads_exist = os.path.exists(rag.uploads_dir)
    
    # Get list of uploaded files
    uploaded_files = []
    if uploads_exist:
        uploaded_files = [f for f in os.listdir(rag.uploads_dir) if f.endswith('.txt')]
    
    # Check Gemini status
    gemini_status = "not configured"
    if gemini_api_key:
        gemini_status = "healthy" if gemini_client else "unhealthy"

    
    return {
        "status": "healthy",
        "backend": "running",
        "llm": {
            "provider": "Google Gemini",
            "model":"gemini-2.5-flash",


            "status": gemini_status
        },
        "vector_store": {
            "exists": stats['index_exists'],
            "total_chunks": stats['total_chunks'],
            "total_documents": stats['total_documents'],
            "dimension": stats['dimension']
        },
        "uploads_directory": {
            "exists": uploads_exist,
            "file_count": len(uploaded_files)
        }
    }

@app.get("/documents")
def list_documents():
    """
    List all uploaded documents.
    Returns list of .txt filenames in uploads directory.
    """
    if not os.path.exists(rag.uploads_dir):
        return {"documents": []}
    
    files = [f for f in os.listdir(rag.uploads_dir) if f.endswith('.txt')]
    
    # Get file sizes
    documents = []
    for filename in files:
        filepath = os.path.join(rag.uploads_dir, filename)
        size = os.path.getsize(filepath)
        documents.append({
            "filename": filename,
            "size_bytes": size
        })
    
    return {"documents": documents, "count": len(documents)}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a .txt document.
    Saves file to uploads/ and adds to FAISS vector store.
    """
    # Validate file type
    if not file.filename.endswith('.txt'):
        raise HTTPException(
            status_code=400,
            detail="Only .txt files are allowed"
        )
    
    # Validate filename
    if not file.filename or file.filename.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )
    
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        # Validate content
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )
        
        # Save file
        filepath = os.path.join(rag.uploads_dir, file.filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Add to vector store
        rag.add_document(file.filename, text)
        
        return {
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "size": len(text)
        }
    
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File encoding error. Please upload UTF-8 encoded text files."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    stats = rag.get_stats()
    if stats['total_documents'] == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Please upload documents first."
        )

    results = rag.search(question, top_k=3)

    if not results:
        return {
            "answer": "No relevant information found in the documents.",
            "source": None,
            "similarity": 0.0,
            "mode": "retrieval"
        }

    top_result = results[0]

    context = "\n\n".join([
        f"From {r['filename']}:\n{r['content']}"
        for r in results[:3]
    ])

    # Generate answer using Gemini if available
    if gemini_client:
        try:
            prompt = f"""Based on the following information from the documents, answer the question.
Only use information from the provided context. If the answer is not in the context, say so.

Context from documents:
{context}

Question: {question}

Answer:"""

            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash",

                contents=prompt
            )

            answer = response.text
            mode = "gemini"

        except Exception as e:
            print(f"Gemini error: {e}")
            answer = top_result['content']
            mode = "retrieval (gemini failed)"
    else:
        answer = top_result['content']
        mode = "retrieval"

    return {
        "answer": answer,
        "source": top_result['filename'],
        "similarity": round(top_result['similarity'], 4),
        "mode": mode,
        "sources_used": [r['filename'] for r in results[:3]]
    }

@app.post("/rebuild")
def rebuild_index():
    """
    Rebuild the vector index from all files in uploads directory.
    Useful if files were added manually.
    """
    try:
        rag.rebuild_index()
        stats = rag.get_stats()
        
        return {
            "message": "Index rebuilt successfully",
            "total_documents": stats['total_documents'],
            "total_chunks": stats['total_chunks']
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Rebuild failed: {str(e)}"
        )

@app.delete("/documents/{filename}")
def delete_document(filename: str):
    """
    Delete a document and rebuild the index.
    Note: This requires rebuilding the entire index.
    """
    filepath = os.path.join(rag.uploads_dir, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    
    try:
        # Delete file
        os.remove(filepath)
        
        # Rebuild index without this file
        rag.rebuild_index()
        
        return {
            "message": "Document deleted successfully",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Delete failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
