from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
import shutil
from typing import Optional, List
import uvicorn
from pathlib import Path
import json

# ML imports
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer
import torch
import pandas as pd
import PyPDF2
from docx import Document

# Initialize FastAPI app
app = FastAPI(title="DynamicRAGSystem - AI Marketing Campaign Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.vercel.app",   # Vercel deployments
        "https://*.netlify.app",  # Netlify deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
llm_pipeline = None
embedding_model = None
documents_db = []

def initialize_models():
    """Initialize Mistral 7B and embedding models"""
    global llm_pipeline, embedding_model
    
    try:
        print("Loading Mistral 7B Instruct model... This may take several minutes.")
        
        # Load Mistral 7B with memory optimization
        model_name = "mistralai/Mistral-7B-Instruct-v0.1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load model with 4-bit quantization to save memory
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_4bit=True,
            trust_remote_code=True
        )
        
        # Create text generation pipeline
        llm_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        print("Mistral 7B model loaded successfully!")
        
        # Load embedding model
        print("Loading embedding model...")
        embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        print("Embedding model loaded successfully!")
        
    except Exception as e:
        print(f"Error loading models: {e}")
        print("Make sure you have enough memory (8GB+ RAM recommended)")

def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Extract text from various file types"""
    try:
        if file_type == '.pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
                
        elif file_type == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
                
        elif file_type == '.csv':
            df = pd.read_csv(file_path)
            return df.to_string()
            
        elif file_type == '.docx':
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
            
        else:
            return ""
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def find_similar_documents(query: str, top_k: int = 3) -> List[str]:
    """Find similar documents using semantic search"""
    if not documents_db or not embedding_model:
        return []
    
    try:
        # Encode query
        query_embedding = embedding_model.encode([query])
        
        # Calculate similarities
        similarities = []
        for doc in documents_db:
            doc_embedding = embedding_model.encode([doc['text']])
            similarity = torch.cosine_similarity(
                torch.tensor(query_embedding), 
                torch.tensor(doc_embedding)
            ).item()
            similarities.append((doc['text'], similarity))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [doc[0] for doc in similarities[:top_k]]
        
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return []

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    initialize_models()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "DynamicRAGSystem API is running!", "status": "healthy"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and index a file for RAG"""
    global documents_db
    
    if not llm_pipeline or not embedding_model:
        raise HTTPException(status_code=500, detail="Models not initialized")
    
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
        
        # Extract text from file
        text = extract_text_from_file(tmp_file_path, file_ext)
        
        if text.strip():
            # Add to documents database
            documents_db.append({
                'filename': file.filename,
                'text': text,
                'file_type': file_ext
            })
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
            return {
                "message": f"File '{file.filename}' uploaded and indexed successfully",
                "filename": file.filename,
                "file_size": len(content),
                "text_length": len(text)
            }
        else:
            os.unlink(tmp_file_path)
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
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
    global llm_pipeline, documents_db
    
    if not llm_pipeline:
        raise HTTPException(status_code=500, detail="LLM model not initialized")
    
    try:
        # Find relevant documents
        relevant_docs = find_similar_documents(query, top_k=3)
        context = "\n\n".join(relevant_docs) if relevant_docs else ""
        
        # Create prompt
        prompt = f"""<s>[INST] You are an expert marketing strategist. Generate a comprehensive marketing campaign based on the following parameters:

Goal: {goal}
Target Audience: {audience}
Tone: {tone}
Specific Query: {query}

{f"Relevant Context from uploaded documents:\n{context}\n" if context else ""}

Please generate a comprehensive marketing campaign that includes:
1. Campaign concept and strategy
2. Key messaging and slogans
3. Target audience insights
4. Channel recommendations
5. Creative ideas and execution suggestions

Make your recommendations specific to the goal, audience, and tone specified. [/INST]"""

        # Generate response
        response = llm_pipeline(
            prompt,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )
        
        campaign_text = response[0]['generated_text']
        # Extract only the response part (after the prompt)
        campaign_text = campaign_text[len(prompt):].strip()
        
        return {
            "campaign": campaign_text,
            "parameters": {
                "goal": goal,
                "audience": audience,
                "tone": tone,
                "query": query
            },
            "context_used": len(relevant_docs)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating campaign: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "llm_available": llm_pipeline is not None,
        "embedding_available": embedding_model is not None,
        "documents_indexed": len(documents_db),
        "llm_provider": "HuggingFace (Mistral-7B-Instruct)"
    }

@app.get("/documents")
async def list_documents():
    """List all indexed documents"""
    return {
        "documents": [
            {
                "filename": doc['filename'],
                "file_type": doc['file_type'],
                "text_length": len(doc['text'])
            }
            for doc in documents_db
        ],
        "total_documents": len(documents_db)
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
