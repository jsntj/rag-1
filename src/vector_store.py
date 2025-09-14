"""
Vector store management for document embeddings
"""
import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document as LangchainDocument
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Manages vector database operations"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=Config.OPENAI_API_KEY,
            model=Config.EMBEDDING_MODEL
        )
        self.vectorstore = None
        self._initialize_vectorstore()
    
    def _initialize_vectorstore(self):
        """Initialize the Chroma vector store"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(Config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
            
            # Initialize Chroma
            self.vectorstore = Chroma(
                persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
                embedding_function=self.embeddings,
                collection_name="pdf_documents"
            )
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    def add_documents(self, documents: List[LangchainDocument]) -> bool:
        """Add documents to the vector store"""
        try:
            if not documents:
                logger.warning("No documents to add")
                return False
            
            # Add documents to Chroma
            self.vectorstore.add_documents(documents)
            
            # Persist the changes
            self.vectorstore.persist()
            
            logger.info(f"Added {len(documents)} documents to vector store")
            return True
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def similarity_search(self, query: str, k: int = None) -> List[LangchainDocument]:
        """Search for similar documents"""
        try:
            if k is None:
                k = Config.TOP_K_RESULTS
            
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = None) -> List[tuple]:
        """Search for similar documents with similarity scores"""
        try:
            if k is None:
                k = Config.TOP_K_RESULTS
            
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            logger.info(f"Found {len(results)} similar documents with scores")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search with score: {e}")
            return []
    
    def get_relevant_documents(self, query: str, k: int = None, threshold: float = None) -> List[LangchainDocument]:
        """Get relevant documents above similarity threshold"""
        try:
            if k is None:
                k = Config.TOP_K_RESULTS
            if threshold is None:
                threshold = Config.SIMILARITY_THRESHOLD
            
            # Get results with scores
            results_with_scores = self.similarity_search_with_score(query, k=k)
            
            # Filter by threshold (lower score = more similar in Chroma)
            relevant_docs = []
            for doc, score in results_with_scores:
                # Chroma uses cosine distance, so lower is better
                # Convert to similarity score (1 - distance)
                similarity = 1 - score
                if similarity >= threshold:
                    relevant_docs.append(doc)
            
            logger.info(f"Found {len(relevant_docs)} relevant documents above threshold {threshold}")
            return relevant_docs
        except Exception as e:
            logger.error(f"Error getting relevant documents: {e}")
            return []
    
    def delete_collection(self):
        """Delete the entire collection"""
        try:
            # This will delete all data in the collection
            self.vectorstore.delete_collection()
            logger.info("Collection deleted successfully")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            # Get collection count
            count = self.vectorstore._collection.count()
            return {
                "document_count": count,
                "persist_directory": Config.CHROMA_PERSIST_DIRECTORY,
                "collection_name": "pdf_documents"
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    def clear_database(self):
        """Clear all documents from the database"""
        try:
            self.delete_collection()
            self._initialize_vectorstore()
            logger.info("Database cleared successfully")
        except Exception as e:
            logger.error(f"Error clearing database: {e}")
