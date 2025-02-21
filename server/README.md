# RAG Chatbot Server

The backend component of the RAG Chatbot, built with FastAPI, LangChain, and Qdrant. Implements RAG (Retrieval-Augmented Generation) for document-based chat.

## Features

- 🚀 FastAPI-based REST API
- 📄 PDF document processing and text extraction
- 🔍 Vector storage with Qdrant
- 🤖 OpenAI integration for embeddings and chat
- 🔄 Asynchronous request handling
- 📊 RAG implementation with LangChain
- 🔒 Environment-based configuration

## Prerequisites

- Python 3.13
- Poetry
- OpenAI API Key
- Docker (optional)

## Configuration

Environment variables (in `app/.env`):
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

## Installation

### Using Docker (Recommended)

The server is part of the main docker-compose setup. See root README for instructions.

### Manual Installation

1. Install Poetry:
   ```bash
   pip install poetry
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run the application:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## Project Structure

```
server/
├── app/
│   ├── agents/         # RAG and chat agent implementations
│   ├── databases/      # Database connections (Qdrant)
│   ├── routers/        # API route handlers
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── utils/          # Helper functions and utilities
│   ├── .env           # Environment configuration
│   ├── .env.example   # Example environment file
│   ├── main.py        # Application entry point
│   └── settings.py    # App settings and configuration
├── Dockerfile         # Docker configuration
├── pyproject.toml     # Poetry dependencies
└── poetry.lock       # Poetry lock file
```

## API Documentation

### Endpoints

#### Files API
- `POST /files/upload`
  - Upload and process PDF files
  - Request: Multipart form data with PDF files
  - Response: Processing status for each file
  ```json
  {
    "message": "Processed 2 files successfully, 0 failed",
    "successful": [
      {"filename": "doc1.pdf", "status": "success"}
    ],
    "failed": []
  }
  ```

#### Chat API
- `POST /chat/`
  - Send a message to the chatbot
  - Request:
    ```json
    {
      "messages": [
        {"content": "What's in the documents?", "sender": "user"}
      ]
    }
    ```
  - Response:
    ```json
    {
      "response": "Based on the documents..."
    }
    ```

Full OpenAPI documentation available at `/docs` when server is running.

## Components

### Document Processing
- PDF text extraction
- Text chunking and preprocessing
- Vector embedding generation
- Storage in Qdrant vector database

### RAG Implementation
- Semantic search in vector store
- Context retrieval
- OpenAI chat completion
- Response generation

### Vector Store
- Persistent Qdrant storage
- Efficient similarity search
- Document metadata management

## Development

1. Set up Poetry environment:
   ```bash
   poetry install
   ```

2. Run with hot-reload:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

3. Access the API at http://localhost:8000

## Testing

Run tests with Poetry:
```bash
poetry run pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[MIT License](../LICENSE)
