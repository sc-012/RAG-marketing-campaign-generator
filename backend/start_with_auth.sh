#!/bin/bash

# Hugging Face Authentication Setup and Backend Start Script
# This script sets up authentication and starts the backend

echo "🚀 Starting RAG Marketing Campaign Generator with Authentication"
echo "=============================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Set environment variables
export HNSWLIB_NO_NATIVE=1

# Check if Hugging Face token is set
if [ -z "$HUGGINGFACE_TOKEN" ]; then
    echo "⚠️  HUGGINGFACE_TOKEN not set. Running authentication setup..."
    python setup_auth.py
    
    if [ $? -ne 0 ]; then
        echo "❌ Authentication setup failed. Please run manually:"
        echo "   python setup_auth.py"
        exit 1
    fi
else
    echo " Hugging Face token found in environment"
fi

# Install huggingface_hub if not already installed
echo "📦 Installing/updating Hugging Face Hub..."
pip install huggingface_hub

# Start the backend
echo "🚀 Starting backend server..."
echo "💡 Make sure you have access to the Mistral model at:"
echo "   https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1"
echo ""

python main.py
