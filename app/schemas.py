from pydantic import BaseModel

class Question(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]