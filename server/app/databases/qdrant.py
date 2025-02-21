from typing import Optional
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from settings import settings
from qdrant_client.http.models import Distance, VectorParams
import os

# Create persistent storage directory
QDRANT_PATH = "./data/qdrant"
os.makedirs(QDRANT_PATH, exist_ok=True)

class Qdrant:
    _instance: Optional['Qdrant'] = None
    _vector_store: Optional[QdrantVectorStore] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the Qdrant client and vector store"""
        # Use persistent storage instead of in-memory
        self.client = QdrantClient(path=QDRANT_PATH)
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model="text-embedding-3-small")

        # Create collection if it doesn't exist
        collections = self.client.get_collections().collections
        if not any(c.name == "documents" for c in collections):
            self.client.create_collection(
                collection_name="documents",
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
            
        self._vector_store = QdrantVectorStore(
            client=self.client,
            collection_name="documents", 
            embedding=self.embeddings
        )

    def get_vector_store(self) -> QdrantVectorStore:
        """Get the vector store instance"""
        if self._vector_store is None:
            self._initialize()
        return self._vector_store


# Create a dependency function for FastAPI
def get_qdrant() -> Qdrant:
    """Dependency function to get the Qdrant instance"""
    return Qdrant()