@echo off
REM DynamicRAGSystem Startup Script for Windows
echo Starting DynamicRAGSystem - AI Marketing Campaign Generator
echo ==============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not installed. Please run setup_ollama.bat first.
    pause
    exit /b 1
)

REM Check if llama2:7b model is available
ollama list | findstr "llama2:7b" >nul
if errorlevel 1 (
    echo ERROR: Llama2:7b model not found. Please run setup_ollama.bat first.
    pause
    exit /b 1
)

REM Check if Ollama service is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Starting Ollama service...
    start "Ollama Service" ollama serve
    timeout /t 3 /nobreak >nul
)

echo Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Start backend in background
echo Starting backend server...
start "Backend Server" cmd /c "python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo Setting up frontend...
cd ..\frontend

REM Install dependencies
echo Installing Node.js dependencies...
npm install

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    echo REACT_APP_API_URL=http://localhost:8000 > .env
)

REM Start frontend
echo Starting frontend server...
start "Frontend Server" cmd /c "npm start"

echo.
echo DynamicRAGSystem is starting up!
echo ==============================================================
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop both servers
pause >nul

REM Stop servers
echo.
echo Stopping servers...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe >nul 2>&1
echo Servers stopped.
pause
