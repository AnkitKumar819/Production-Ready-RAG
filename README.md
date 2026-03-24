# Production Ready RAG Chatbot

A complete Retrieval-Augmented Generation (RAG) chatbot application that allows users to upload documents and ask questions about their content. Built with FastAPI backend and Streamlit frontend, deployed on Railway and Streamlit Cloud.

## Features

- 📄 Document Upload: Support for PDF and TXT files
- 🤖 AI-Powered Q&A: Uses OpenAI GPT-4 for intelligent responses
- 🔍 Semantic Search: FAISS vector store for efficient document retrieval
- 🌐 Web Interface: Streamlit frontend for easy interaction
- 🚀 Production Ready: Docker containerization and cloud deployment

## Architecture

- **Backend**: FastAPI with LangChain, OpenAI, and FAISS
- **Frontend**: Streamlit web application
- **Vector Store**: FAISS for document embeddings
- **LLM**: OpenAI GPT-4
- **Deployment**: Railway (backend) + Streamlit Cloud (frontend)

## Quick Start

### Prerequisites

- Python 3.14+
- OpenAI API key
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Production-Ready-RAG.git
   cd Production-Ready-RAG
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the backend**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Run the frontend** (in another terminal)
   ```bash
   streamlit run streamlit_app.py
   ```

## API Endpoints

- `GET /`: Status information
- `GET /health`: Health check
- `POST /upload`: Upload document (PDF/TXT)
- `POST /ask`: Ask question about uploaded documents
- `GET /docs`: API documentation

## Deployment

### Backend (Railway)

1. Push code to GitHub
2. Connect to Railway
3. Set environment variables in Railway dashboard:
   - `OPENAI_API_KEY`
4. Deploy

### Frontend (Streamlit Cloud)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub repo
3. Set main file to `streamlit_app.py`
4. Add secret: `API_URL` = your Railway app URL
5. Deploy

## Usage

1. Open the Streamlit app
2. Upload a PDF or TXT document
3. Ask questions about the document content
4. Get AI-powered answers with source references

## Configuration

- **Chunk Size**: 500 characters (configurable in `rag.py`)
- **Overlap**: 50 characters
- **Top K Results**: 4 documents retrieved
- **Model**: GPT-4 with temperature 0.7

## Security Notes

- File uploads are validated for type and size
- API keys are stored securely as environment variables
- No user authentication implemented (add for production use)

## Development

### Project Structure

```
Production_Ready_RAG/
├── app/
│   ├── main.py          # FastAPI application
│   ├── rag.py           # RAG pipeline
│   ├── embedding.py     # OpenAI embeddings
│   ├── llm.py           # GPT-4 integration
│   ├── vector_store.py  # FAISS manager
│   ├── schemas.py       # Pydantic models
│   ├── config.py        # Configuration
│   └── ui.py            # Alternative UI (deprecated)
├── streamlit_app.py     # Streamlit frontend
├── Dockerfile           # Container config
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
└── README.md           # This file
```

### Adding Features

- Modify `app/rag.py` for RAG logic changes
- Update `streamlit_app.py` for UI improvements
- Add new endpoints in `app/main.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test locally
5. Submit a pull request

## License

MIT License - see LICENSE file for details
