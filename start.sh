#!/bin/bash

# DynamicRAGSystem Startup Script
echo "Starting DynamicRAGSystem - AI Marketing Campaign Generator"
echo "=============================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if Ollama is installed and running
if ! command -v ollama &> /dev/null; then
    echo "ERROR: Ollama is not installed. Please run ./setup_ollama.sh first."
    exit 1
fi

# Check if llama2:7b model is available
if ! ollama list | grep -q "llama2:7b"; then
    echo "ERROR: Llama2:7b model not found. Please run ./setup_ollama.sh first."
    exit 1
fi

# Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 3
fi

echo "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Start backend in background
echo "Starting backend server..."
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "Setting up frontend..."
cd ../frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
fi

# Start frontend
echo "Starting frontend server..."
npm start &
FRONTEND_PID=$!

echo ""
echo "DynamicRAGSystem is starting up!"
echo "=============================================================="
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers stopped."
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
