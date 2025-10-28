# 🛠️ Development Guide

## Project Overview

This is a **local RAG (Retrieval-Augmented Generation)** system that enables users to chat with their documents using AI. The system processes documents locally, creates embeddings, and uses Google's Gemini AI for intelligent question answering with full conversation memory.

## Architecture Deep Dive

### Backend (FastAPI)

**main.py** - API server with endpoints:
- `POST /upload` - Accepts multiple files, validates types, stores them
- `POST /chat` - Receives questions, queries RAG pipeline, returns answers with sources
- `GET /report` - Generates PDF report of conversation history
- `POST /clear` - Resets conversation memory
- `GET /health` - Status check endpoint

**rag_pipeline.py** - Document processing pipeline:
1. **Text Extraction**: Uses file-specific extractors (pdfplumber, python-docx, pypandoc)
2. **Chunking**: Splits text into overlapping chunks using RecursiveCharacterTextSplitter
3. **Embedding**: Creates vector embeddings using Gemini embedding model
4. **Storage**: Persists embeddings in local ChromaDB vector store
5. **Retrieval**: Searches for relevant chunks based on query similarity
6. **Generation**: Uses Gemini to generate contextual answers

**memory.py** - Conversation memory management:
- Single global `ConversationBufferMemory` instance
- Maintains full conversation history for context
- Used by ConversationalRetrievalChain for multi-turn conversations

**report_generator.py** - PDF report creation:
- Uses ReportLab to create formatted PDFs
- Includes conversation history with Q&A formatting
- Adds metadata (timestamp, exchange count)

### Frontend (Streamlit)

**app.py** - User interface:
- File upload widget with multi-file support
- Chat interface with message history
- Real-time API communication with backend
- Report download functionality
- Session state management

### Data Flow

```
User uploads files
    ↓
Files saved to data/uploads/
    ↓
Text extracted from each file
    ↓
Text split into chunks (1000 chars, 200 overlap)
    ↓
Chunks embedded using Gemini
    ↓
Embeddings stored in ChromaDB (data/vectorstore/)
    ↓
User asks question
    ↓
Question embedded
    ↓
Similar chunks retrieved (k=4)
    ↓
Chunks + conversation history → Gemini
    ↓
Answer generated and returned
    ↓
Q&A saved to memory
```

## Key Technologies

### LangChain Components
- `RecursiveCharacterTextSplitter` - Intelligent text chunking
- `ConversationalRetrievalChain` - RAG with memory
- `ConversationBufferMemory` - Full conversation tracking
- `GoogleGenerativeAIEmbeddings` - Gemini embeddings
- `ChatGoogleGenerativeAI` - Gemini chat model

### Vector Store (ChromaDB)
- Local, file-based vector database
- Persistent storage in `data/vectorstore/`
- Supports semantic similarity search
- No external database needed

### Document Loaders
- **PDF**: pdfplumber (better text extraction than PyPDF2)
- **DOCX**: python-docx (native Word support)
- **RTF**: pypandoc (converts via Pandoc)
- **TXT**: Native Python file handling

## Configuration Options

### rag_pipeline.py
```python
CHUNK_SIZE = 1000          # Size of text chunks
CHUNK_OVERLAP = 200        # Overlap between chunks
VECTORSTORE_PATH = "data/vectorstore"
```

### Retriever Settings
```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}  # Number of chunks to retrieve
)
```

### Gemini Settings
```python
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,  # Creativity level (0-1)
    convert_system_message_to_human=True
)
```

## Extending the System

### Adding New File Types

1. Create extractor function in `rag_pipeline.py`:
```python
def extract_text_from_pptx(file_path: str) -> str:
    # Implementation
    pass
```

2. Add to extractors dict:
```python
extractors = {
    '.pdf': extract_text_from_pdf,
    '.pptx': extract_text_from_pptx,  # Add new
    # ...
}
```

3. Update allowed extensions in `main.py`:
```python
allowed_extensions = {'.pdf', '.docx', '.rtf', '.png', '.txt', '.pptx'}
```

### Adding Image Analysis (PNG/JPG)

Use Gemini Vision API for images:

```python
from langchain_google_genai import ChatGoogleGenerativeAI

def extract_text_from_image(file_path: str) -> str:
    # Load image
    import base64
    with open(file_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()
    
    # Use Gemini Vision
    vision_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-vision",
        google_api_key=GOOGLE_API_KEY
    )
    
    prompt = "Extract all text and describe this image:"
    response = vision_model.invoke([
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:image/png;base64,{image_data}"}
    ])
    
    return response.content
```

### Adding User Sessions

Replace global memory with session-based memory:

```python
# memory.py
_session_memories = {}

def get_memory(session_id: str) -> ConversationBufferMemory:
    if session_id not in _session_memories:
        _session_memories[session_id] = ConversationBufferMemory(...)
    return _session_memories[session_id]
```

### Persisting Memory to Database

Use SQLite to persist conversations:

```python
import sqlite3
import json

def save_memory_to_db(session_id: str, memory: ConversationBufferMemory):
    conn = sqlite3.connect('data/conversations.db')
    cursor = conn.cursor()
    
    messages = [msg.dict() for msg in memory.chat_memory.messages]
    
    cursor.execute('''
        INSERT INTO conversations (session_id, messages, timestamp)
        VALUES (?, ?, datetime('now'))
    ''', (session_id, json.dumps(messages)))
    
    conn.commit()
    conn.close()
```

### Adding Authentication

Use FastAPI dependencies:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

def verify_token(credentials = Depends(security)):
    token = credentials.credentials
    # Verify token
    if not valid_token(token):
        raise HTTPException(status_code=401)
    return token

@app.post("/chat")
async def chat(request: ChatRequest, token = Depends(verify_token)):
    # Protected endpoint
    pass
```

## Testing

### Unit Tests
Create `backend/tests/test_rag_pipeline.py`:

```python
import pytest
from rag_pipeline import extract_text_from_pdf

def test_pdf_extraction():
    text = extract_text_from_pdf("test.pdf")
    assert len(text) > 0
    assert "expected content" in text
```

### Integration Tests
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_endpoint():
    with open("test.pdf", "rb") as f:
        response = client.post("/upload", files={"files": f})
    assert response.status_code == 200
```

### Load Testing
Use locust or ab (Apache Bench):

```bash
ab -n 100 -c 10 http://localhost:8000/health
```

## Deployment

### Docker
Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
Production `.env`:

```
GOOGLE_API_KEY=production_key
LOG_LEVEL=INFO
VECTORSTORE_PATH=/data/vectorstore
MAX_UPLOAD_SIZE=10485760
```

## Performance Optimization

### Caching
Add caching to frequently accessed data:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_embeddings(text: str):
    # Cache embeddings for repeated queries
    pass
```

### Async Processing
Use background tasks for large uploads:

```python
from fastapi import BackgroundTasks

@app.post("/upload")
async def upload_files(
    files: List[UploadFile],
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(process_documents, file_paths)
    return {"status": "processing"}
```

### Database Optimization
Use FAISS instead of Chroma for faster similarity search:

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("data/faiss_index")
```

## Troubleshooting

### Common Issues

**"No module named X"**
- Run `pip install -r requirements.txt`

**"Pandoc not found"**
- Install Pandoc from pandoc.org
- RTF files won't work without it

**"API quota exceeded"**
- Check Gemini API quota
- Add rate limiting

**"Vector store not found"**
- Upload documents first
- Check `data/vectorstore/` exists

**Memory issues with large files**
- Reduce CHUNK_SIZE
- Process files in batches
- Increase system RAM

## Best Practices

1. **Always validate file uploads** - Check size, type, content
2. **Handle API errors gracefully** - Add retry logic
3. **Log everything** - Use proper logging levels
4. **Version your embeddings** - Track model versions
5. **Monitor performance** - Add metrics and monitoring
6. **Secure API keys** - Never commit .env files
7. **Test edge cases** - Empty files, huge files, malformed content

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details
