@echo off
echo ========================================
echo   Starting Frontend...
echo ========================================
echo.

cd frontend

if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_frontend.bat first.
    pause
    exit
)

call venv\Scripts\activate.bat
echo Frontend will open in your browser...
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py
