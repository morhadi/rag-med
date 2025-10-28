"""
FastAPI backend for Local RAG Assistant
Endpoints: /upload, /chat, /report
"""
import os
import shutil
from pathlib import Path
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag_pipeline import process_documents, query_rag
from memory import get_memory, clear_memory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Local RAG Assistant API")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directories
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "active", "message": "RAG Assistant API is running"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple documents for processing
    Accepts: PDF, DOCX, RTF, PNG, TXT
    """
    try:
        uploaded_files = []
        
        for file in files:
            # Validate file type
            allowed_extensions = {'.pdf', '.docx', '.rtf', '.png', '.txt'}
            file_ext = Path(file.filename).suffix.lower()
            
            if file_ext not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"File type {file_ext} not supported. Allowed: {allowed_extensions}"
                )
            
            # Save uploaded file
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append(str(file_path))
            logger.info(f"Uploaded file: {file.filename}")
        
        # Process documents through RAG pipeline
        result = process_documents(uploaded_files)
        
        return {
            "status": "success",
            "files_uploaded": len(uploaded_files),
            "files": [Path(f).name for f in uploaded_files],
            "chunks_created": result.get("chunks_count", 0),
            "message": "Documents processed and indexed successfully"
        }
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint with RAG and conversation memory
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Query RAG system with memory
        response = query_rag(request.message)
        
        return ChatResponse(
            response=response.get("answer", ""),
            sources=response.get("sources", [])
        )
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report")
async def generate_report():
    """
    Generate and download PDF report of the conversation
    """
    try:
        from report_generator import create_report_pdf
        
        memory = get_memory()
        conversation_history = memory.chat_memory.messages
        
        if not conversation_history:
            raise HTTPException(
                status_code=400,
                detail="No conversation history to generate report"
            )
        
        # Generate PDF report
        report_path = create_report_pdf(conversation_history)
        
        return FileResponse(
            path=report_path,
            media_type="application/pdf",
            filename="rag_conversation_report.pdf"
        )
    
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_conversation():
    """
    Clear conversation memory and start fresh
    """
    try:
        clear_memory()
        return {"status": "success", "message": "Conversation memory cleared"}
    except Exception as e:
        logger.error(f"Clear memory error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Detailed health check"""
    memory = get_memory()
    message_count = len(memory.chat_memory.messages)
    
    return {
        "status": "healthy",
        "vectorstore_exists": Path("data/vectorstore").exists(),
        "conversation_messages": message_count,
        "uploads_count": len(list(UPLOAD_DIR.glob("*")))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
