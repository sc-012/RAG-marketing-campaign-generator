#!/bin/bash

# Ollama Setup Script for DynamicRAGSystem
echo "🦙 Setting up Ollama with Llama2:7b for DynamicRAGSystem"
echo "========================================================"

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
    ollama --version
else
    echo "📦 Installing Ollama..."
    
    # Install Ollama based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        echo "Installing Ollama for macOS..."
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        echo "Installing Ollama for Linux..."
        curl -fsSL https://ollama.ai/install.sh | sh
    else
        echo "❌ Unsupported operating system. Please install Ollama manually from https://ollama.ai"
        exit 1
    fi
fi

# Start Ollama service
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Pull Llama2:7b model
echo "📥 Downloading Llama2:7b model (this may take a few minutes)..."
ollama pull llama2:7b

# Verify installation
echo "🔍 Verifying installation..."
if ollama list | grep -q "llama2:7b"; then
    echo "✅ Llama2:7b model installed successfully!"
else
    echo "❌ Failed to install Llama2:7b model"
    exit 1
fi

# Test the model
echo "🧪 Testing the model..."
TEST_RESPONSE=$(ollama run llama2:7b "Hello, this is a test." 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ Model is working correctly!"
    echo "Sample response: ${TEST_RESPONSE:0:100}..."
else
    echo "❌ Model test failed"
    exit 1
fi

echo ""
echo "🎉 Ollama setup complete!"
echo "========================="
echo "✅ Ollama service is running (PID: $OLLAMA_PID)"
echo "✅ Llama2:7b model is ready"
echo "✅ DynamicRAGSystem can now use local LLM"
echo ""
echo "To stop Ollama service: kill $OLLAMA_PID"
echo "To start Ollama manually: ollama serve"
echo "To test the model: ollama run llama2:7b 'Your prompt here'"
echo ""
echo "🚀 You can now start the DynamicRAGSystem backend!"
