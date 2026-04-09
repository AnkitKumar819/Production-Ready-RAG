from pydantic import BaseModel

from typing import Optional

class Question(BaseModel):
    question: str
    source_doc: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: list = []