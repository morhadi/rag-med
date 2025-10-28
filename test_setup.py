"""
Test script to verify RAG Assistant setup
Run this after installation to check all components
"""
import sys
import importlib
from pathlib import Path

def check_import(module_name, package_name=None):
    """Check if a Python package is installed"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError:
        print(f"❌ {package_name or module_name} - NOT INSTALLED")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if Path(dirpath).is_dir():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False

def main():
    print("=" * 60)
    print("  LOCAL RAG ASSISTANT - ENVIRONMENT CHECK")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Python version
    print("🐍 Python Version Check:")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        all_passed = False
    print()
    
    # Core dependencies
    print("📦 Backend Dependencies:")
    deps = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("pdfplumber", "pdfplumber (PDF support)"),
        ("docx", "python-docx (DOCX support)"),
        ("pypandoc", "pypandoc (RTF support)"),
        ("langchain", "LangChain"),
        ("langchain_google_genai", "LangChain Google GenAI"),
        ("chromadb", "ChromaDB"),
        ("reportlab", "ReportLab (PDF reports)"),
        ("dotenv", "python-dotenv"),
    ]
    
    for module, name in deps:
        if not check_import(module, name):
            all_passed = False
    print()
    
    # Frontend dependencies
    print("🎨 Frontend Dependencies:")
    frontend_deps = [
        ("streamlit", "Streamlit"),
        ("requests", "Requests"),
    ]
    
    for module, name in frontend_deps:
        if not check_import(module, name):
            all_passed = False
    print()
    
    # File structure
    print("📁 File Structure:")
    files = [
        ("backend/main.py", "Backend main.py"),
        ("backend/rag_pipeline.py", "RAG pipeline"),
        ("backend/memory.py", "Memory module"),
        ("backend/report_generator.py", "Report generator"),
        ("backend/requirements.txt", "Backend requirements"),
        ("backend/.env.example", "Environment template"),
        ("frontend/app.py", "Frontend app"),
        ("frontend/requirements.txt", "Frontend requirements"),
        ("README.md", "README"),
    ]
    
    for filepath, desc in files:
        if not check_file_exists(filepath, desc):
            all_passed = False
    print()
    
    # Directories
    print("📂 Data Directories:")
    dirs = [
        ("backend/data/uploads", "Uploads directory"),
        ("backend/data/texts", "Texts directory"),
        ("backend/data/vectorstore", "Vectorstore directory"),
    ]
    
    for dirpath, desc in dirs:
        if not check_directory_exists(dirpath, desc):
            all_passed = False
    print()
    
    # Environment check
    print("🔐 Environment Configuration:")
    if check_file_exists("backend/.env", ".env file"):
        try:
            with open("backend/.env", "r") as f:
                content = f.read()
                if "GOOGLE_API_KEY" in content and "your_" not in content:
                    print("✅ API key appears to be configured")
                else:
                    print("⚠️  API key needs to be set in .env")
                    all_passed = False
        except:
            pass
    else:
        print("⚠️  Create .env from .env.example and add your API key")
        all_passed = False
    print()
    
    # Pandoc check (optional for RTF)
    print("🔧 Optional Tools:")
    try:
        import subprocess
        result = subprocess.run(["pandoc", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Pandoc (for RTF support)")
        else:
            print("⚠️  Pandoc not found (RTF files won't work)")
    except:
        print("⚠️  Pandoc not found (RTF files won't work)")
    print()
    
    # Final verdict
    print("=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print()
        print("You're ready to run the application:")
        print("  1. cd backend && uvicorn main:app --reload")
        print("  2. cd frontend && streamlit run app.py")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before running.")
        print("Run: pip install -r backend/requirements.txt")
        print("Run: pip install -r frontend/requirements.txt")
    print("=" * 60)

if __name__ == "__main__":
    main()
