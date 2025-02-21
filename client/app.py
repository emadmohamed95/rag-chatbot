import os
import json
import streamlit as st
import httpx
from streamlit_chat import message
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Constants
API_URL = os.getenv("API_URL", "http://localhost:8000")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
TIMEOUT_SECONDS = None  # No timeout

print(f"API_URL: {API_URL}")

# Page config
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stChatMessage {
        padding: 1rem;
    }
    .stChatInput {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

def upload_files(files):
    """Upload files to the server"""
    if not files:
        return
        
    with st.spinner("Uploading and processing files..."):
        files_data = [
            ("files", (file.name, file.getvalue(), "application/pdf"))
            for file in files
            if file.size <= MAX_FILE_SIZE
        ]
        
        if not files_data:
            st.error("All files exceed the maximum size limit of 5MB")
            return
            
        try:
            response = httpx.post(
                f"{API_URL}/files/upload", 
                files=files_data,
                timeout=TIMEOUT_SECONDS
            )
            response.raise_for_status()
            result = response.json()
            
            successful = len(result.get("successful", []))
            failed = len(result.get("failed", []))
            
            if successful > 0:
                st.success(f"Successfully processed {successful} files")
                # Update uploaded files list
                st.session_state.uploaded_files.extend([
                    f["filename"] for f in result.get("successful", [])
                ])
            if failed > 0:
                st.error(f"Failed to process {failed} files")
                
        except Exception as e:
            st.error(f"Error uploading files: {str(e)}")

async def send_message(message: str):
    """Send message to the chatbot API"""
    try:
        # Add user message to state
        st.session_state.messages.append({"content": message, "sender": "user"})
        
        # Prepare the request
        data = {
            "messages": st.session_state.messages
        }
        
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.post(
                f"{API_URL}/chat/",
                json=data
            )
            response.raise_for_status()
            
            # Get the response
            result = response.json()
            bot_message = result["response"]
            
            # Add bot response to state
            st.session_state.messages.append({
                "content": bot_message,
                "sender": "ai"
            })
            
    except Exception as e:
        st.error(f"Error communicating with the chatbot: {str(e)}")
        return None

def display_chat_history():
    """Display chat history using streamlit_chat for user messages and markdown for AI responses"""
    for i, msg in enumerate(st.session_state.messages):
        if msg["sender"] == "user":
            message(
                msg["content"],
                is_user=True,
                key=f"msg_{i}"
            )
        else:
            message(
                msg["content"],
                is_user=False,
                key=f"msg_{i}"
            )

def main():
    st.title("🤖 RAG Chatbot")
    
    # Sidebar for file upload
    with st.sidebar:
        st.subheader("📄 Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload PDF files to chat about (max 5MB each)"
        )
        
        if uploaded_files:
            if st.button("Process Files", type="primary"):
                upload_files(uploaded_files)
                
        # Display uploaded files
        if st.session_state.uploaded_files:
            st.subheader("📚 Processed Files")
            for file in st.session_state.uploaded_files:
                st.text(f"• {file}")
        
        # Clear chat button
        if st.session_state.messages and st.button("Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat area
    st.subheader("💬 Chat")
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        display_chat_history()
    
    # Chat input
    st.markdown("---")
    if prompt := st.chat_input(
        "Ask about the documents...",
        disabled=not (st.session_state.uploaded_files or st.session_state.messages)
    ):
        if st.session_state.uploaded_files or st.session_state.messages:
            with st.spinner("Thinking..."):
                asyncio.run(send_message(prompt))
            st.rerun()
        else:
            st.warning("Please upload some documents first!")

if __name__ == "__main__":
    main() 