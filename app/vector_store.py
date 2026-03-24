from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from .config import VECTOR_DIR
import os


class VectorStoreManager:
    def __init__(self, embeddings):
        """Initialize vector store manager with embeddings."""
        self.embeddings = embeddings
        self.vector_dir = VECTOR_DIR
        
        # Try to load existing vectorstore
        if os.path.exists(os.path.join(self.vector_dir, "index.faiss")):
            self.store = FAISS.load_local(self.vector_dir, embeddings, allow_dangerous_deserialization=True)
        else:
            # Create empty store (will be populated on first add)
            self.store = None

    def add_documents(self, documents: list):
        """Add documents to the vector store."""
        if self.store is None:
            self.store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.store.add_documents(documents)
        
        # Save the updated store
        self.store.save_local(self.vector_dir)

    def similarity_search(self, query: str, k: int = 4) -> list:
        """Search for similar documents."""
        if self.store is None:
            return []
        return self.store.similarity_search(query, k=k)
