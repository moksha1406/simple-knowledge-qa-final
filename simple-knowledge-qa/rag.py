"""
RAG module for document embedding and retrieval using FAISS.
No LLM, no OpenAI - just pure retrieval.
"""

import os
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle

class SimpleRAG:
    def __init__(self, 
                 uploads_dir: str = "uploads",
                 vector_store_dir: str = "vector_store",
                 model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG system with FAISS vector store.
        
        Args:
            uploads_dir: Directory where uploaded files are stored
            vector_store_dir: Directory where FAISS index is stored
            model_name: Sentence transformer model name
        """
        self.uploads_dir = uploads_dir
        self.vector_store_dir = vector_store_dir
        self.index_path = os.path.join(vector_store_dir, "faiss.index")
        self.metadata_path = os.path.join(vector_store_dir, "metadata.pkl")
        
        # Create directories
        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(vector_store_dir, exist_ok=True)
        
        # Load embedding model
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
        # Load or create FAISS index
        self.index = None
        self.metadata = []  # List of (filename, chunk_text)
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create new one."""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            print("Loading existing FAISS index...")
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            print(f"Loaded index with {len(self.metadata)} chunks")
        else:
            print("Creating new FAISS index...")
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
    
    def _save_index(self):
        """Save FAISS index and metadata to disk."""
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        print(f"Saved index with {len(self.metadata)} chunks")
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into chunks by words.
        
        Args:
            text: Input text
            chunk_size: Number of words per chunk
            
        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def add_document(self, filename: str, content: str):
        """
        Add a document to the vector store.
        
        Args:
            filename: Name of the document
            content: Text content of the document
        """
        # Chunk the document
        chunks = self._chunk_text(content)
        print(f"Adding {len(chunks)} chunks from {filename}")
        
        # Generate embeddings for all chunks
        embeddings = self.model.encode(chunks, convert_to_numpy=True)
        
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        
        # Store metadata
        for chunk in chunks:
            self.metadata.append({
                'filename': filename,
                'content': chunk
            })
        
        # Save index
        self._save_index()
    
    def search(self, query: str, top_k: int = 1) -> List[Dict]:
        """
        Search for relevant chunks using FAISS.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of results with filename, content, and similarity score
        """
        if self.index.ntotal == 0:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        
        # Search in FAISS
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Prepare results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):  # Valid index
                # Convert L2 distance to similarity score (0-1, higher is better)
                similarity = 1 / (1 + distance)
                
                results.append({
                    'filename': self.metadata[idx]['filename'],
                    'content': self.metadata[idx]['content'],
                    'similarity': float(similarity),
                    'rank': i + 1
                })
        
        return results
    
    def rebuild_index(self):
        """
        Rebuild FAISS index from all files in uploads directory.
        Useful when files are added directly to uploads folder.
        """
        # Reset index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        
        # Process all .txt files
        txt_files = [f for f in os.listdir(self.uploads_dir) if f.endswith('.txt')]
        
        for filename in txt_files:
            filepath = os.path.join(self.uploads_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.add_document(filename, content)
        
        print(f"Rebuilt index with {len(txt_files)} documents")
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with stats
        """
        num_files = len(set(meta['filename'] for meta in self.metadata))
        
        return {
            'total_chunks': len(self.metadata),
            'total_documents': num_files,
            'index_exists': os.path.exists(self.index_path),
            'dimension': self.dimension
        }
    
    def clear_index(self):
        """Clear the entire index and metadata."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        self._save_index()
        print("Index cleared")
