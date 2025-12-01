# Retrieval-Augmented Generation (RAG) Marketing Campaign Generator

A fullstack MVP application that uses Retrieval-Augmented Generation (RAG) to generate AI-powered marketing campaigns based on uploaded documents and user parameters.

## Features

- **Document Upload & Indexing**: Upload PDFs, CSVs, and text files to build a knowledge base
- **AI-Powered Campaign Generation**: Generate tailored marketing campaigns using RAG technology
- **Parameter-Based Customization**: Specify campaign goals, target audience, and tone
- **Modern UI**: Built with React and Material-UI for a professional user experience
- **Vector Search**: Uses ChromaDB for efficient document retrieval
- **Hugging Face Embeddings**: Leverages state-of-the-art sentence transformers

## Architecture

### Backend (Python + FastAPI)
- **FastAPI**: Modern, fast web framework for building APIs
- **LlamaIndex**: Orchestrates RAG pipeline and document processing
- **ChromaDB**: Vector database for storing and retrieving embeddings
- **Hugging Face**: Sentence transformers for document embeddings
- **Ollama + Llama2:7b**: Local Large Language Model for campaign generation

### Frontend (React + Material-UI)
- **React**: Modern JavaScript library for building user interfaces
- **Material-UI**: Comprehensive component library for consistent design
- **Axios**: HTTP client for API communication

## 📁 Project Structure

```
V4_React_Marketing/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── chroma_db/          # ChromaDB storage (created automatically)
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Custom styles
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Global styles
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8+ 
- Node.js 16+
- Ollama (for local LLM)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Ollama (local LLM):**
   ```bash
   # Run the Ollama setup script
   ./setup_ollama.sh
   
   # Or manually:
   # 1. Install Ollama from https://ollama.ai
   # 2. Run: ollama pull llama2:7b
   # 3. Start Ollama: ollama serve
   ```

5. **Run the backend server:**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   echo "REACT_APP_API_URL=http://localhost:8000" > .env
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

1. **Upload Documents**: Use the file upload section to add marketing documents (PDFs, CSVs, text files) to build your knowledge base.

2. **Set Parameters**: Choose your campaign goal, target audience, and tone from the dropdown menus.

3. **Enter Query**: Describe what you want to promote or achieve in the query field.

4. **Generate Campaign**: Click "Generate Campaign" to get AI-powered marketing recommendations based on your uploaded documents and parameters.

## 📡 API Endpoints

### POST /upload
Upload and index a file for RAG processing.

**Request:**
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
Generate marketing campaign based on parameters and query.

**Request:**
- `goal`: Campaign goal (e.g., "Brand Awareness")
- `audience`: Target audience (e.g., "Gen Z")
- `tone`: Campaign tone (e.g., "Inspirational")
- `query`: Specific campaign query

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

## Deployment

### Frontend (Vercel)

1. **Connect your GitHub repository to Vercel**
2. **Set build settings:**
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

3. **Set environment variables:**
   - `REACT_APP_API_URL`: Your backend API URL

### Backend (Local/Cloud)

The backend can be deployed on any cloud platform that supports Python:

1. **Heroku**: Add `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
2. **Railway**: Deploy directly from GitHub
3. **AWS/GCP/Azure**: Use container services or serverless functions

## Configuration

### Environment Variables

**Backend:**
- Ollama service running locally (no API key required)

**Frontend:**
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000)

### Supported File Types

- PDF (.pdf)
- Text (.txt)
- CSV (.csv)
- Markdown (.md)
- Word Document (.docx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Ollama Service Error**: Make sure Ollama is installed and running with `ollama serve`
2. **ChromaDB Connection Error**: Ensure the `chroma_db` directory has write permissions
3. **CORS Errors**: Check that the frontend URL is added to the CORS origins in `main.py`
4. **File Upload Errors**: Verify file type is supported and file size is reasonable

### Getting Help

- Check the API health endpoint: `GET /health`
- Review the console logs for detailed error messages
- Ensure all dependencies are properly installed

## 🔮 Future Enhancements

- [ ] Support for more file types (PowerPoint, Excel)
- [ ] Batch file upload
- [ ] Campaign templates and presets
- [ ] Export campaigns to various formats
- [ ] User authentication and campaign history
- [ ] Advanced analytics and insights
- [ ] Integration with social media platforms
