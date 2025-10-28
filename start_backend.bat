@echo off
echo ========================================
echo   Starting Backend Server...
echo ========================================
echo.

cd backend

if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_backend.bat first.
    pause
    exit
)

if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your GOOGLE_API_KEY
    pause
    exit
)

call venv\Scripts\activate.bat
echo Backend starting at http://localhost:8000
echo API docs at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
uvicorn main:app --reload
