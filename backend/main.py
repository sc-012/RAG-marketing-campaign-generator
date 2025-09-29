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
from llama_index.llms.openai import OpenAI
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

# Upload progress tracking
upload_progress = {"status": "idle", "message": "", "progress": 0}

def initialize_rag_components():
    """Initialize RAG components on startup"""
    global vector_index, llm, embed_model, chroma_client, collection
    
    try:
        # Initialize ChromaDB
        chroma_client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model with optimized settings
        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"  # Force CPU usage for stability
        )
        Settings.embed_model = embed_model
        
        # Initialize OpenAI LLM
        print("Initializing OpenAI API...")
        
        llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        Settings.llm = llm
        
        print("OpenAI API initialized successfully!")
        
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
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
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
        global upload_progress
        upload_progress = {"status": "uploading", "message": f"Starting upload of {file.filename}...", "progress": 10}
        print(f"Starting upload of {file.filename}...")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        upload_progress = {"status": "processing", "message": f"File saved, size: {len(content)} bytes", "progress": 30}
        print(f"File saved, size: {len(content)} bytes")
        
        # Create a temporary directory for LlamaIndex
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy file to temp directory
            temp_file_path = os.path.join(temp_dir, file.filename)
            shutil.copy2(tmp_file_path, temp_file_path)
            
            upload_progress = {"status": "processing", "message": "Loading document with LlamaIndex...", "progress": 50}
            print("Loading document with LlamaIndex...")
            # Load document with LlamaIndex - optimized for speed
            documents = SimpleDirectoryReader(
                temp_dir,
                file_extractor={
                    ".pdf": "PyMuPDFReader",  # Faster PDF reader
                    ".txt": "TextFileReader",
                    ".csv": "CSVReader",
                    ".md": "MarkdownReader",
                    ".docx": "DocxReader"
                }
            ).load_data()
            
            upload_progress = {"status": "indexing", "message": f"Document loaded, {len(documents)} chunks created", "progress": 70}
            print(f"Document loaded, {len(documents)} chunks created")
            
            # Add documents to the vector index in batches for better performance
            batch_size = 5  # Process in smaller batches
            total_batches = (len(documents) - 1) // batch_size + 1
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                for doc in batch:
                    # Truncate very long documents to improve speed
                    if len(doc.text) > 4000:  # Limit text length
                        doc.text = doc.text[:4000] + "..."
                    vector_index.insert(doc)
                batch_num = i // batch_size + 1
                progress = 70 + (batch_num / total_batches) * 20
                upload_progress = {"status": "indexing", "message": f"Processed batch {batch_num}/{total_batches}", "progress": int(progress)}
                print(f"Processed batch {batch_num}/{total_batches}")
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        upload_progress = {"status": "completed", "message": f"Upload completed for {file.filename}", "progress": 100}
        print(f"Upload completed for {file.filename}")
        return {
            "message": f"File '{file.filename}' uploaded and indexed successfully",
            "filename": file.filename,
            "file_size": len(content),
            "chunks_processed": len(documents)
        }
        
    except Exception as e:
        upload_progress = {"status": "error", "message": f"Error processing file: {str(e)}", "progress": 0}
        print(f"Error processing file: {str(e)}")
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
        # Create a structured query for better marketing content generation
        enhanced_query = f"""
        Create a marketing campaign for:
        - Goal: {goal}
        - Audience: {audience}
        - Tone: {tone}
        - Focus: {query}
        
        Provide a clear, professional marketing strategy with:
        1. Campaign concept
        2. Key messages
        3. Target channels
        4. Creative suggestions
        
        Keep the response concise and actionable.
        """
        
        # Query the vector index with optimized settings
        query_engine = vector_index.as_query_engine(
            response_mode="compact",
            similarity_top_k=2,  # Further reduced for speed
            streaming=False,  # Disable streaming for faster response
            verbose=False  # Reduce logging overhead
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
        "llm_provider": "OpenAI (GPT-3.5-turbo)",
        "embed_model_available": embed_model is not None,
        "chroma_available": chroma_client is not None
    }

@app.get("/upload-progress")
async def get_upload_progress():
    """Get current upload progress"""
    global upload_progress
    return upload_progress

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
