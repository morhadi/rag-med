# 🤖 Local RAG Assistant with Gemini + LangChain

A **local Retrieval-Augmented Generation (RAG)** system that allows you to chat with your documents using Google's Gemini AI. Upload PDFs, DOCX, RTF, and text files, then ask questions with full conversation memory!

## ✨ Features

- 📄 **Multi-format Support**: PDF, DOCX, RTF, TXT, PNG
- 🔍 **Semantic Search**: Find relevant information across all documents
- 💬 **Conversational Memory**: Full context awareness throughout the session
- 📊 **PDF Reports**: Generate downloadable conversation summaries
- 🔒 **Local First**: All processing happens locally (except Gemini API calls)
- 🚀 **Easy to Use**: Simple web interface with Streamlit

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Streamlit  │ ───> │   FastAPI    │ ───> │   Gemini    │
│  Frontend   │ <─── │   Backend    │ <─── │     API     │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ├─> Text Extraction (pdfplumber, python-docx)
                            ├─> Chunking (LangChain)
                            ├─> Embeddings (Gemini)
                            └─> Vector Store (Chroma)
```

## 📋 Prerequisites

- Python 3.9+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Pandoc (for RTF support): [Download here](https://pandoc.org/installing.html)

## 🚀 Quick Start

### 1. Clone & Setup

```bash
cd "c:\Users\Hadi\Downloads\hiring task\hiring task\dataset"
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 3. Frontend Setup

```bash
cd ..\frontend
pip install -r requirements.txt
```

### 4. Run the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
streamlit run app.py
```

### 5. Access the Application

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 Usage Guide

### Upload Documents
1. Click "Browse files" in the sidebar
2. Select one or more documents (PDF, DOCX, RTF, TXT, PNG)
3. Click "Process Documents"
4. Wait for processing to complete

### Chat with Documents
1. Type your question in the chat input at the bottom
2. Press Enter or click Send
3. View the AI response with source citations
4. Ask follow-up questions — the assistant remembers context!

### Generate Report
1. After chatting, click "Download PDF Report" in the sidebar
2. Click "Save Report" to download the PDF
3. The report includes all conversation exchanges with formatting

### Clear & Start Fresh
- Click "Clear Conversation" in the sidebar to reset memory
- Upload new documents to add to the existing knowledge base

## 🛠️ API Endpoints

### Backend API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload and process documents |
| `/chat` | POST | Send a message and get AI response |
| `/report` | GET | Generate and download PDF report |
| `/clear` | POST | Clear conversation memory |
| `/health` | GET | Check system status |

## 📁 Project Structure

```
rag-assistant/
│
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag_pipeline.py      # Document processing & RAG logic
│   ├── memory.py            # Conversation memory management
│   ├── report_generator.py  # PDF report creation
│   ├── requirements.txt     # Backend dependencies
│   ├── .env.example         # Environment template
│   └── data/
│       ├── uploads/         # Uploaded files
│       ├── texts/           # Extracted text
│       ├── vectorstore/     # Chroma database
│       └── reports/         # Generated PDFs
│
├── frontend/
│   ├── app.py              # Streamlit interface
│   └── requirements.txt    # Frontend dependencies
│
└── README.md
```

## 🧰 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI |
| **Frontend** | Streamlit |
| **LLM** | Google Gemini 1.5 Pro |
| **Embeddings** | Gemini Embeddings |
| **Vector Store** | ChromaDB |
| **RAG Framework** | LangChain |
| **Document Processing** | pdfplumber, python-docx, pypandoc |
| **Report Generation** | ReportLab |

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
GOOGLE_API_KEY=your_api_key_here
```

### Customization

Edit `rag_pipeline.py` to adjust:
- `CHUNK_SIZE = 1000` - Size of text chunks
- `CHUNK_OVERLAP = 200` - Overlap between chunks
- Temperature and other LLM parameters

## 🔧 Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that `.env` file exists with valid API key
- Make sure port 8000 is available

### Frontend can't connect
- Verify backend is running on http://localhost:8000
- Check the API_BASE_URL in `frontend/app.py`

### RTF files not working
- Install Pandoc: https://pandoc.org/installing.html
- Verify installation: `pandoc --version`

### Gemini API errors
- Check your API key is valid
- Ensure you have API quota remaining
- Verify internet connection

## 🎯 Example Questions

After uploading documents, try asking:

- "What is the main topic of these documents?"
- "Summarize the key points from the uploaded files"
- "What are the differences between [concept A] and [concept B]?"
- "Can you explain [specific topic] mentioned in the documents?"
- "What recommendations are made in the documents?"

## 🔒 Privacy & Security

- All document processing happens locally on your machine
- Only API calls to Gemini require internet connection
- No data is stored in the cloud
- Vector database stored locally in `data/vectorstore/`

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

This is a demonstration project following the instructions in `INSTRUCTIONS.md`. Feel free to extend it with:

- Additional file format support (PPTX, CSV)
- User authentication and sessions
- Multiple conversation threads
- Advanced search and filtering
- Docker containerization

## 🙏 Acknowledgments

Built with:
- [Google Gemini](https://ai.google.dev/)
- [LangChain](https://python.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [ChromaDB](https://www.trychroma.com/)

---

**Need help?** Check the API documentation at http://localhost:8000/docs when the backend is running!
