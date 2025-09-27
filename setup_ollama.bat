@echo off
REM Ollama Setup Script for DynamicRAGSystem (Windows)
echo 🦙 Setting up Ollama with Llama2:7b for DynamicRAGSystem
echo ========================================================

REM Check if Ollama is already installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Ollama...
    echo Please download and install Ollama from https://ollama.ai/download
    echo After installation, run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Ollama is already installed
    ollama --version
)

REM Start Ollama service
echo 🚀 Starting Ollama service...
start "Ollama Service" ollama serve

REM Wait for Ollama to start
echo ⏳ Waiting for Ollama to start...
timeout /t 5 /nobreak >nul

REM Pull Llama2:7b model
echo 📥 Downloading Llama2:7b model (this may take a few minutes)...
ollama pull llama2:7b

REM Verify installation
echo 🔍 Verifying installation...
ollama list | findstr "llama2:7b" >nul
if errorlevel 1 (
    echo ❌ Failed to install Llama2:7b model
    pause
    exit /b 1
) else (
    echo ✅ Llama2:7b model installed successfully!
)

REM Test the model
echo 🧪 Testing the model...
ollama run llama2:7b "Hello, this is a test." >nul 2>&1
if errorlevel 1 (
    echo ❌ Model test failed
    pause
    exit /b 1
) else (
    echo ✅ Model is working correctly!
)

echo.
echo 🎉 Ollama setup complete!
echo =========================
echo ✅ Ollama service is running
echo ✅ Llama2:7b model is ready
echo ✅ DynamicRAGSystem can now use local LLM
echo.
echo To test the model: ollama run llama2:7b "Your prompt here"
echo.
echo 🚀 You can now start the DynamicRAGSystem backend!
pause
