from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
import shutil
from typing import Optional, List
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# RAG and ML imports
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    StorageContext,
    Settings
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
import chromadb
from chromadb.config import Settings as ChromaSettings

# Initialize FastAPI app
app = FastAPI(title="DynamicRAGSystem - AI Marketing Campaign Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for RAG components
vector_index = None
llm = None
embed_model = None
chroma_client = None
collection = None

def initialize_rag_components():
    """Initialize RAG components on startup"""
    global vector_index, llm, embed_model, chroma_client, collection
    
    try:
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        Settings.embed_model = embed_model
        
        # Initialize LLM (using Mistral 7B Instruct with memory optimization)
        print("Loading DistilGPT-2 model... This should be quick.")
        
        llm = HuggingFaceLLM(
            model_name="distilgpt2",
            tokenizer_name="distilgpt2",
            context_window=1024,  # Smaller context window
            max_new_tokens=256,   # Reduced max tokens
            model_kwargs={
                "dtype": "auto",
                "trust_remote_code": True,
            },
            generate_kwargs={
                "do_sample": True, 
                "temperature": 0.7, 
                "top_p": 0.9,
                "repetition_penalty": 1.1
            },
        )
        Settings.llm = llm
        
        print("DistilGPT-2 model loaded successfully!")
        
        # Try to load existing collection or create new one
        try:
            collection = chroma_client.get_collection("marketing_docs")
            vector_store = ChromaVectorStore(chroma_collection=collection)
            vector_index = VectorStoreIndex.from_vector_store(vector_store)
            print("Loaded existing vector index")
        except:
            # Create new collection if none exists
            collection = chroma_client.create_collection("marketing_docs")
            vector_store = ChromaVectorStore(chroma_collection=collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            vector_index = VectorStoreIndex([], storage_context=storage_context)
            print("Created new vector index")
            
    except Exception as e:
        print(f"Error initializing RAG components: {e}")
        print("Make sure you have enough memory (8GB+ RAM recommended)")
        # Fallback initialization
        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        Settings.embed_model = embed_model

# Initialize RAG components on startup
try:
    initialize_rag_components()
    print("RAG system initialized successfully!")
except Exception as e:
    print(f"RAG initialization failed: {e}")
    print("Continuing with basic functionality...")
    # Set basic fallback values
    vector_index = None
    llm = None
    embed_model = None
    chroma_client = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "DynamicRAGSystem API is running!", "status": "healthy"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and index a file for RAG"""
    global vector_index, collection
    
    if not vector_index:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    # Check file type
    allowed_types = [".pdf", ".txt", ".csv", ".md", ".docx"]
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not supported. Allowed types: {allowed_types}"
        )
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Create a temporary directory for LlamaIndex
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy file to temp directory
            temp_file_path = os.path.join(temp_dir, file.filename)
            shutil.copy2(tmp_file_path, temp_file_path)
            
            # Load document with LlamaIndex
            documents = SimpleDirectoryReader(temp_dir).load_data()
            
            # Add documents to the vector index
            for doc in documents:
                vector_index.insert(doc)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return {
            "message": f"File '{file.filename}' uploaded and indexed successfully",
            "filename": file.filename,
            "file_size": len(content)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/query")
async def query_campaign(
    goal: str = Form(...),
    audience: str = Form(...),
    tone: str = Form(...),
    query: str = Form(...)
):
    """Generate marketing campaign based on query and parameters"""
    global vector_index, llm
    
    if not vector_index:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    
    try:
        # Create a comprehensive query combining user input with parameters
        enhanced_query = f"""
        Marketing Campaign Request:
        Goal: {goal}
        Target Audience: {audience}
        Tone: {tone}
        Specific Query: {query}
        
        Please generate a comprehensive marketing campaign that includes:
        1. Campaign concept and strategy
        2. Key messaging and slogans
        3. Target audience insights
        4. Channel recommendations
        5. Creative ideas and execution suggestions
        
        Base your recommendations on the provided context and make them specific to the goal, audience, and tone specified.
        """
        
        # Query the vector index
        query_engine = vector_index.as_query_engine(
            response_mode="compact",
            similarity_top_k=3  # Reduced to save memory
        )
        
        response = query_engine.query(enhanced_query)
        
        return {
            "campaign": response.response,
            "parameters": {
                "goal": goal,
                "audience": audience,
                "tone": tone,
                "query": query
            },
            "context_used": len(response.source_nodes) if hasattr(response, 'source_nodes') else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating campaign: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "rag_initialized": vector_index is not None,
        "llm_available": llm is not None,
        "llm_provider": "HuggingFace (Mistral-7B-Instruct)",
        "embed_model_available": embed_model is not None,
        "chroma_available": chroma_client is not None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
