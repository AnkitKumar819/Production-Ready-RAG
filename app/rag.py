from .embedding import get_embeddings
from .vector_store import VectorStoreManager
from .llm import get_llm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader


class RAGPipeline:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vector_store = VectorStoreManager(self.embeddings)
        self.llm = get_llm()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

    def ingest(self, file_path: str):
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)

        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        self.vector_store.add_documents(chunks)

    def ask(self, question: str) -> dict:
        docs = self.vector_store.similarity_search(question)
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
        Use the context below to answer the question.

        Context:
        {context}

        Question:
        {question}
        """

        response = self.llm.invoke(prompt)
        
        # Extract sources from documents
        sources = []
        for doc in docs:
            if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                sources.append(doc.metadata['source'])
            else:
                sources.append("Unknown source")
        
        return {
            "answer": response.content,
            "sources": sources
        }
