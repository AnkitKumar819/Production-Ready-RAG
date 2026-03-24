from langchain_openai import ChatOpenAI
from .config import OPENAI_API_KEY


def get_llm():
    """Initialize and return OpenAI LLM."""
    return ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4",
        temperature=0.7
    )
