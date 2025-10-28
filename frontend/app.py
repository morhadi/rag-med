"""
Streamlit Frontend for Local RAG Assistant
Features: File upload, chat interface, report download
"""
import streamlit as st
import requests
from pathlib import Path
import time

# Backend API configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Local RAG Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1a73e8;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1976d2;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .source-tag {
        background-color: #fff3cd;
        padding: 0.2rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.85rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'documents_uploaded' not in st.session_state:
    st.session_state.documents_uploaded = False

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_files(files):
    """Upload files to backend"""
    try:
        files_data = [("files", (file.name, file, file.type)) for file in files]
        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files_data,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def send_message(message):
    """Send chat message to backend"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Chat error: {str(e)}")
        return None

def download_report():
    """Download conversation report"""
    try:
        response = requests.get(f"{API_BASE_URL}/report", timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        st.error(f"Report generation error: {str(e)}")
        return None

def clear_conversation():
    """Clear conversation memory"""
    try:
        response = requests.post(f"{API_BASE_URL}/clear", timeout=10)
        response.raise_for_status()
        st.session_state.messages = []
        return True
    except Exception as e:
        st.error(f"Clear error: {str(e)}")
        return False

# Main UI
st.markdown("<h1 class='main-header'>🤖 Local RAG Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Upload documents, ask questions, and generate reports — all locally with Gemini AI</p>", unsafe_allow_html=True)

# Check backend status
if not check_backend_health():
    st.error("⚠️ Backend server is not running! Please start the backend with: `cd backend && uvicorn main:app --reload`")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("📁 Document Upload")
    
    uploaded_files = st.file_uploader(
        "Upload your documents",
        type=["pdf", "docx", "rtf", "txt", "png"],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, RTF, TXT, PNG"
    )
    
    if uploaded_files:
        if st.button("📤 Process Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                result = upload_files(uploaded_files)
                if result:
                    st.success(f"✅ Processed {result['files_uploaded']} files")
                    st.info(f"Created {result['chunks_created']} text chunks")
                    st.session_state.documents_uploaded = True
    
    st.divider()
    
    # Report generation
    st.header("📊 Generate Report")
    if st.button("📥 Download PDF Report", use_container_width=True, disabled=len(st.session_state.messages) == 0):
        with st.spinner("Generating report..."):
            pdf_data = download_report()
            if pdf_data:
                st.download_button(
                    label="💾 Save Report",
                    data=pdf_data,
                    file_name=f"rag_report_{time.strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    st.divider()
    
    # Clear conversation
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        if clear_conversation():
            st.success("Conversation cleared!")
            st.rerun()
    
    st.divider()
    
    # Status
    st.header("ℹ️ Status")
    st.metric("Documents Uploaded", "✅" if st.session_state.documents_uploaded else "❌")
    st.metric("Messages", len(st.session_state.messages))

# Main chat interface
st.header("💬 Chat Interface")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"<div class='chat-message user-message'><strong>You:</strong><br>{message['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            sources_html = ""
            if message.get('sources'):
                sources_html = "<br><strong>📚 Sources:</strong> " + " ".join(
                    [f"<span class='source-tag'>{s}</span>" for s in message['sources']]
                )
            
            st.markdown(
                f"<div class='chat-message assistant-message'><strong>Assistant:</strong><br>{message['content']}{sources_html}</div>",
                unsafe_allow_html=True
            )

# Chat input
user_input = st.chat_input("Ask a question about your documents...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get response from backend
    with st.spinner("Thinking..."):
        response = send_message(user_input)
        
        if response:
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["response"],
                "sources": response.get("sources", [])
            })
    
    # Rerun to update chat display
    st.rerun()

# Help section
with st.expander("ℹ️ How to use"):
    st.markdown("""
    ### Getting Started
    1. **Upload Documents**: Use the sidebar to upload PDF, DOCX, RTF, TXT, or PNG files
    2. **Click Process**: Wait for the documents to be processed and indexed
    3. **Ask Questions**: Type your questions in the chat box below
    4. **View Sources**: See which documents were used to answer your questions
    5. **Generate Report**: Download a PDF summary of your conversation
    
    ### Features
    - 🔍 **Semantic Search**: Find relevant information across all your documents
    - 💾 **Conversation Memory**: The assistant remembers previous messages
    - 📊 **PDF Reports**: Export your conversation as a formatted PDF
    - 🔒 **Local Processing**: All data stays on your machine (except Gemini API calls)
    
    ### Tips
    - Upload multiple documents at once for comprehensive answers
    - Ask follow-up questions — the assistant remembers context
    - Use "Clear Conversation" to start fresh
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 0.9rem;'>Powered by Gemini AI & LangChain | Local RAG Assistant v1.0</p>",
    unsafe_allow_html=True
)
