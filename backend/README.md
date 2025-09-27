# DynamicRAGSystem Backend

FastAPI backend for the AI Marketing Campaign Generator using RAG (Retrieval-Augmented Generation) technology.

## 🏗️ Architecture

- **FastAPI**: Modern, fast web framework
- **LlamaIndex**: RAG orchestration and document processing
- **ChromaDB**: Vector database for embeddings storage
- **Hugging Face**: Sentence transformers for document embeddings
- **OpenAI**: Large Language Model for campaign generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

4. **Run the server:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📡 API Documentation

Once the server is running, visit:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key for LLM functionality

### ChromaDB Storage

The application automatically creates a `chroma_db` directory for vector storage. This directory will contain:
- Vector embeddings of uploaded documents
- Metadata for document retrieval
- Index files for fast searching

## 📊 API Endpoints

### POST /upload
Upload and index a file for RAG processing.

**Parameters:**
- `file`: Multipart file upload (PDF, CSV, TXT, MD, DOCX)

**Response:**
```json
{
  "message": "File uploaded and indexed successfully",
  "filename": "example.pdf",
  "file_size": 1024
}
```

### POST /query
Generate marketing campaign based on parameters.

**Parameters:**
- `goal`: Campaign goal (form data)
- `audience`: Target audience (form data)
- `tone`: Campaign tone (form data)
- `query`: Campaign query (form data)

**Response:**
```json
{
  "campaign": "Generated campaign content...",
  "parameters": {
    "goal": "Brand Awareness",
    "audience": "Gen Z",
    "tone": "Inspirational",
    "query": "Promote eco-friendly sneakers"
  },
  "context_used": 3
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "rag_initialized": true,
  "llm_available": true,
  "embed_model_available": true,
  "chroma_available": true
}
```

## 🔍 RAG Pipeline

1. **Document Upload**: Files are uploaded via the `/upload` endpoint
2. **Text Extraction**: LlamaIndex extracts text from various file formats
3. **Embedding Generation**: Hugging Face embeddings convert text to vectors
4. **Vector Storage**: ChromaDB stores embeddings with metadata
5. **Query Processing**: User queries are embedded and matched against stored vectors
6. **Context Retrieval**: Most relevant document chunks are retrieved
7. **LLM Generation**: OpenAI LLM generates campaigns using retrieved context

## 🛠️ Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Upload a file
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@example.pdf"

# Generate campaign
curl -X POST "http://localhost:8000/query" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "goal=Brand Awareness&audience=Gen Z&tone=Inspirational&query=Promote eco-friendly sneakers"
```

## 🚀 Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t dynamic-rag-backend .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key dynamic-rag-backend
```

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   ```
   Error: OpenAI API key not found
   ```
   Solution: Set the `OPENAI_API_KEY` environment variable

2. **ChromaDB Permission Error**:
   ```
   Error: Permission denied creating chroma_db directory
   ```
   Solution: Ensure write permissions in the current directory

3. **Memory Issues with Large Files**:
   ```
   Error: Out of memory processing large file
   ```
   Solution: Process smaller files or increase available memory

4. **CORS Errors**:
   ```
   Error: CORS policy blocks request
   ```
   Solution: Add your frontend URL to CORS origins in `main.py`

### Logs and Debugging

Enable debug logging by setting:
```bash
export LOG_LEVEL=DEBUG
```

## 📈 Performance Optimization

1. **ChromaDB Configuration**: Adjust collection settings for your use case
2. **Embedding Model**: Consider using smaller models for faster processing
3. **Batch Processing**: Process multiple documents in batches
4. **Caching**: Implement Redis caching for frequent queries

## 🔒 Security Considerations

1. **API Key Management**: Store OpenAI API key securely
2. **File Validation**: Validate file types and sizes
3. **Rate Limiting**: Implement rate limiting for production use
4. **Input Sanitization**: Sanitize user inputs to prevent injection attacks

## 📚 Dependencies

See `requirements.txt` for the complete list of dependencies. Key packages:

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `llama-index`: RAG orchestration
- `chromadb`: Vector database
- `sentence-transformers`: Embeddings
- `openai`: LLM integration
