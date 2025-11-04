# Interview Assistance Chatbot

A comprehensive chatbot system designed to help users prepare for job interviews, answer career-related questions, and provide guidance on resumes, skills, and interview techniques.

## Features

- **Domain-specific chatbot**: Trained to provide clear, accurate, and actionable answers using retrieved context
- **Document processing**: Supports PDF and DOCX file uploads for knowledge base creation
- **Vector search**: Uses FAISS for efficient similarity search over document chunks
- **WebSocket communication**: Real-time chat interface
- **Streamlit UI**: User-friendly web interface for database management and chat
- **FastAPI backend**: RESTful API for document processing and retrieval

## Architecture

The system consists of several components:

1. **Agent (`agent.py`)**: WebSocket server handling chat interactions with Groq LLM
2. **FastAPI Backend (`main.py`)**: API endpoints for document upload and processing
3. **Streamlit UI (`streamlit/main.py`)**: Web interface for database management
4. **Processing Modules**:
   - `processing/chunker.py`: Document text chunking
   - `processing/embedder.py`: Text embedding generation
   - `processing/retriever.py`: Vector similarity search
5. **Data Storage**: FAISS index and metadata stored in `data/embeddings/`

## Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd interview-assistance-chabot
```

2. Create and activate virtual environment:
```bash
python -m venv env
env\Scripts\activate  # On Windows
# source env/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192  # or your preferred model
```

## Usage

### Running the System

Start the components in separate terminals:

1. **Start the Agent (WebSocket server)**:
```bash
python agent.py
```

2. **Start the FastAPI backend**:
```bash
uvicorn main:app --reload --port 8080
```

3. **Start the Streamlit UI**:
```bash
streamlit run streamlit\main.py
```

### Database Management

1. Open the Streamlit UI at `http://localhost:8501`
2. Upload PDF or DOCX documents using the "Database Updater" page
3. The system will process documents, create embeddings, and update the FAISS index

### Chat Interface

- Access the chat interface through the Streamlit UI
- Ask questions related to job interviews, career advice, resume tips, etc.
- The chatbot will retrieve relevant context from uploaded documents and provide informed answers

## API Endpoints

- `POST /upload`: Upload and process documents
- `GET /health`: Health check endpoint

## Data Flow

1. Documents are uploaded via Streamlit UI
2. Text is extracted and chunked into smaller pieces
3. Embeddings are generated for each chunk
4. Chunks and embeddings are stored in FAISS index
5. User queries are embedded and searched against the index
6. Relevant chunks are retrieved and used as context for LLM responses

## Configuration

- **Chunk size**: 300 characters (configurable in `processing/chunker.py`)
- **Chunk overlap**: 50 characters
- **Top-k retrieval**: 5 most similar chunks per query
- **Embedding model**: Sentence Transformers (via LangChain)

## Troubleshooting

- Ensure all environment variables are set correctly
- Check that the virtual environment is activated
- Verify that all required ports (8080, 8501, 8765) are available
- Make sure the `data/embeddings/` directory exists and contains `index.faiss` and `metadata.json`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]
