# RAG Chatbot Client

The frontend component of the RAG Chatbot, built with Streamlit. Provides a user-friendly interface for document upload and chat interaction.

## Features

- 📄 Document upload interface with drag-and-drop support
- 💬 Real-time chat interface with message history
- 🎨 Clean and responsive design
- 🔄 Automatic chat updates
- 📱 Mobile-friendly layout
- 🚫 File size validation (5MB limit per file)
- 📊 Upload status feedback

## Prerequisites

- Python 3.11 or higher
- pip or Docker

## Configuration

Environment variables (in `.env`):
```bash
API_URL=http://localhost:8000  # URL of the backend server
```

## Installation

### Using Docker (Recommended)

The client is part of the main docker-compose setup. See root README for instructions.

### Manual Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
client/
├── app.py              # Main Streamlit application
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration
└── README.md          # This file
```

## Components

### Document Upload
- Located in the sidebar
- Supports multiple PDF files
- Shows upload progress and status
- Lists processed documents

### Chat Interface
- Real-time message display
- Markdown support for AI responses
- Chat history management
- Clear chat functionality

## Development

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run with hot-reload:
   ```bash
   streamlit run app.py
   ```

3. Access the application at http://localhost:8501

## API Integration

The client communicates with the backend through:

- `POST /files/upload`: Document upload endpoint
- `POST /chat/`: Chat message endpoint

See the server README for detailed API documentation.

## Error Handling

- File size validation
- API connection errors
- Upload status feedback
- Chat error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[MIT License](../LICENSE) 