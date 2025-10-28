@echo off
echo ========================================
echo  Local RAG Assistant - Frontend Setup
echo ========================================
echo.

cd frontend

echo Checking if virtual environment exists...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the frontend, run:
echo   cd frontend
echo   venv\Scripts\activate.bat
echo   streamlit run app.py
echo.
echo Or simply run: start_frontend.bat
echo.
pause
