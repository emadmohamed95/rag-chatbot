# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload documents and chat with an AI about their contents. Built with FastAPI, Streamlit, and OpenAI.

## Features

- 📄 **Document Upload**: Upload and process PDF documents
- 💬 **Interactive Chat**: Chat with AI about the uploaded documents
- 🔍 **Smart Retrieval**: Uses RAG to provide accurate, context-aware responses
- 🎯 **Vector Search**: Powered by Qdrant for efficient semantic search
- 🚀 **Real-time Processing**: Asynchronous processing of documents and chat
- 📱 **Modern UI**: Clean and responsive interface built with Streamlit

## Architecture

The project consists of two main components:

1. **Backend Server (FastAPI)**
   - Handles document processing and embedding
   - Manages vector storage with Qdrant
   - Processes chat messages using OpenAI
   - Implements RAG for accurate responses

2. **Frontend Client (Streamlit)**
   - Provides user interface for document upload
   - Implements chat interface
   - Handles real-time communication with backend

## Prerequisites

- Docker and Docker Compose
- OpenAI API Key

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-chatbot
   ```

2. Set up environment variables:
   ```bash
   # In server/app/.env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Build and run with Docker Compose:
   ```bash
   docker compose up --build
   ```

4. Access the applications:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage

1. **Upload Documents**
   - Click "Upload Documents" in the sidebar
   - Select one or more PDF files (max 5MB each)
   - Click "Process Files" to upload and process

2. **Chat with the Bot**
   - Type your question in the chat input
   - The bot will respond using information from your documents
   - Clear chat history using the "Clear Chat" button

## Project Structure

```
rag-chatbot/
├── client/             # Streamlit frontend
├── server/             # FastAPI backend
├── docker-compose.yml  # Docker composition
└── README.md          # This file
```

See individual README files in client/ and server/ directories for component-specific details.

## API Documentation

The backend API provides the following endpoints:

### Files API
- `POST /files/upload`: Upload and process PDF files
  - Accepts multiple PDF files
  - Returns processing status for each file

### Chat API
- `POST /chat/`: Send a message to the chatbot
  - Accepts chat history and new message
  - Returns AI-generated response

Full API documentation is available at http://localhost:8000/docs when the server is running.

## Development

For local development:

1. Set up Python virtual environments for both client and server
2. Install dependencies using pip (client) and poetry (server)
3. Run the applications separately:
   ```bash
   # Server
   cd server
   poetry install
   poetry run uvicorn app.main:app --reload

   # Client
   cd client
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)