#!/bin/bash

# Production Start Script for RAG Marketing Campaign Generator
# This script is designed for production deployment

echo "🚀 Starting RAG Marketing Campaign Generator (Production Mode)"
echo "============================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Set production environment variables
export HNSWLIB_NO_NATIVE=1
export PYTHONPATH=$(pwd)

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Please edit .env file with your actual values:"
        echo "   nano .env"
        echo "   Then run this script again."
        exit 1
    else
        echo "❌ .env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# Load environment variables
echo "🔐 Loading environment variables from .env file..."
set -a
source .env
set +a

# Verify required environment variables
if [ -z "$HUGGINGFACE_TOKEN" ]; then
    echo "❌ HUGGINGFACE_TOKEN not set in .env file"
    exit 1
fi

echo " Environment variables loaded successfully"

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Start the backend with production settings
echo "🚀 Starting backend server in production mode..."
echo "💡 Make sure you have access to the Mistral model at:"
echo "   https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1"
echo ""

# Use uvicorn with production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
