from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import os

from .rag import RAGPipeline
from .schemas import Question, ChatResponse

load_dotenv()

app = FastAPI(title="Production RAG API")

rag = RAGPipeline()

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
    content = await file.read()
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(content)

    rag.ingest(file_path)
    os.remove(file_path)

    return {"message": "File processed successfully"}

@app.post("/ask", response_model=ChatResponse)
def ask_question(request: Question):
    answer = rag.ask(request.question)
    return ChatResponse(answer=answer, sources=[])