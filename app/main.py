from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import os

from .schemas import Question, ChatResponse

load_dotenv()

app = FastAPI(title="Production RAG API")

# Lazy load RAG pipeline to avoid startup errors
_rag_instance = None

def get_rag():
    """Get or create RAG pipeline instance (lazy loading)"""
    global _rag_instance
    if _rag_instance is None:
        from .rag import RAGPipeline
        _rag_instance = RAGPipeline()
    return _rag_instance

@app.get("/")
def root():
    """Root endpoint - API is running"""
    return {
        "status": "✅ Production RAG API is running!",
        "message": "Welcome to the RAG Chatbot API",
        "endpoints": {
            "docs": "/docs",
            "upload": "/upload (POST)",
            "ask": "/ask (POST)",
            "health": "/health (GET)"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as f:
            f.write(content)

        rag = get_rag()
        rag.ingest(file_path)
        os.remove(file_path)

        return {"message": "File processed successfully"}
    except Exception as e:
        return {"error": str(e), "message": "File upload failed"}

@app.post("/ask", response_model=ChatResponse)
def ask_question(request: Question):
    try:
        rag = get_rag()
        answer = rag.ask(request.question)
        return ChatResponse(answer=answer, sources=[])
    except Exception as e:
        return ChatResponse(answer=f"Error: {str(e)}", sources=[])