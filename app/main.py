from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

from .schemas import Question, ChatResponse

load_dotenv()

app = FastAPI(title="Production RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
    """Serve the frontend interface"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"status": "Frontend not found", "message": "Please make sure static/index.html exists"}

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

@app.post("/clear")
def clear_knowledge_base():
    try:
        rag = get_rag()
        rag.clear()
        return {"success": True, "message": "Knowledge base cleared successfully"}
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"error": str(e), "message": "Failed to clear knowledge base"})

@app.post("/ask", response_model=ChatResponse)
def ask_question(request: Question):
    try:
        rag = get_rag()
        result = rag.ask(request.question, source_doc=request.source_doc)
        return ChatResponse(answer=result["answer"], sources=result["sources"])
    except Exception as e:
        return ChatResponse(answer=f"Error: {str(e)}", sources=[])