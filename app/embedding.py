from langchain_openai import OpenAIEmbeddings
from .config import OPENAI_API_KEY


def get_embeddings():
    """Initialize and return OpenAI embeddings."""
    return OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
