# 🧭 INSTRUCTIONS.md — Local RAG Assistant with Gemini + LangChain

## 🎯 Project Goal

Build a **local Retrieval-Augmented Generation (RAG)** system that can:

1. Let the user **upload multi-format documents** (PDF, DOCX, RTF, PNG flowcharts, etc.).
2. **Extract, embed, and store** their text content locally.
3. **Chat conversationally** with full memory (single persistent session).
4. **Generate a downloadable PDF report** of the conversation or findings.
5. **Run entirely offline** except for Gemini API calls.

---

## 🧩 Core Architecture

### 1. Frontend (local)

* Simple UI with **file upload + chat box + “Download Report”** button.
* Recommended frameworks: **Gradio** (simplest) or **Streamlit**.
* Sends API calls to backend endpoints:

  * `POST /upload`
  * `POST /chat`
  * `GET /report`

### 2. Backend

Run a **FastAPI server** exposing REST endpoints.

```
/upload  → handle file ingestion & text extraction
/chat    → conversational RAG with memory
/report  → generate and return PDF of session
```

### 3. RAG Pipeline (LangChain-powered)

1. **Extract text**

   * PDFs → `pdfplumber`
   * DOCX → `python-docx`
   * RTF → `pypandoc`
   * PNG (flowcharts/tables) → only if needed, via Gemini Vision API
2. **Chunk text** → `RecursiveCharacterTextSplitter`
3. **Embed** → Gemini embeddings (`gemini-1.5-pro-embedding`)
4. **Store** → Local **Chroma** or **FAISS** vector store
5. **Retrieve + Generate** → Gemini (`gemini-1.5-pro`)
6. **Memory** → `ConversationBufferMemory` kept globally

---

## ⚙️ Memory Strategy

* Maintain a single in-memory `ConversationBufferMemory` instance for the whole app.
* No user sessions or external DBs.
* LangChain automatically appends past messages for each new query.

---

## 📦 Directory Layout

```
rag-assistant/
│
├── backend/
│   ├── main.py              # FastAPI entry
│   ├── rag_pipeline.py      # Text extraction, embeddings, retrieval
│   ├── memory.py            # Global LangChain memory instance
│   ├── requirements.txt
│   └── data/
│       ├── uploads/         # Original user files
│       ├── texts/           # Extracted text chunks
│       └── vectorstore/     # Chroma/FAISS database
│
├── frontend/
│   ├── app.py or app.jsx    # Streamlit or React/Gradio
│   └── assets/
│
└── INSTRUCTIONS.md
```

---

## 🧰 Recommended Tech Stack

| Component            | Library / Tool                          | Reason                                             |
| -------------------- | --------------------------------------- | -------------------------------------------------- |
| **Backend**          | FastAPI                                 | Lightweight, async, perfect for local API          |
| **Frontend**         | Gradio / Streamlit                      | Fast local UI prototyping                          |
| **LLM + Embeddings** | Gemini (via `langchain-google-genai`)   | Unified ecosystem for text, embeddings, and vision |
| **Vector Store**     | Chroma or FAISS                         | Local, file-based vector database                  |
| **Text Extractors**  | `pdfplumber`, `python-docx`, `pypandoc` | Handles PDFs, DOCX, RTF                            |
| **Memory**           | LangChain `ConversationBufferMemory`    | Persistent context for full chat                   |
| **Report Generator** | `reportlab` or `python-docx`            | Create downloadable PDF summaries                  |

---

## 🧠 Workflow Summary

1. User uploads multiple files from frontend.
2. Backend extracts text → splits → embeds → stores in vector DB.
3. User asks questions → RAG retrieves relevant chunks → Gemini generates answers.
4. Memory keeps track of conversation context automatically.
5. On request, backend compiles conversation + references into a report and returns it as PDF.

---

## 🚀 Run Instructions

1. **Backend Setup**

   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend Setup**

   ```bash
   cd frontend
   streamlit run app.py
   ```

   *(or use `gradio app.py` / React dev server depending on setup)*

3. **Access**

   * Backend API: `http://localhost:8000`
   * Frontend UI: `http://localhost:8501` (Streamlit) or configured port

---

## 🔒 Notes

* No cloud DB or user authentication needed.
* Only Gemini API calls require internet.
* Keep your Gemini API key in `.env`:

  ```
  GOOGLE_API_KEY=your_key_here
  ```
* Everything else runs locally — embeddings, retrieval, memory, and chat context.

---

## 🧠 Future Enhancements

* Add session-level memory persistence using `sqlite` or Redis.
* Support more file types (e.g. `.pptx`, `.csv`).
* Add semantic search or keyword filtering on documents.
* Deploy using Docker for reproducibility.

---

**→ Objective for VS Code agent:**
Use this `INSTRUCTIONS.md` as guidance to generate:

* a working FastAPI backend (`main.py`, `rag_pipeline.py`, `memory.py`)
* a simple Streamlit or Gradio chat frontend
* a local Chroma or FAISS vector store integration
* Gemini API integration for both embeddings and chat
