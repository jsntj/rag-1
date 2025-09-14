"""
Configuration settings for the RAG PDF Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("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")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
    # Vector Database
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Application Settings
    APP_NAME = os.getenv("APP_NAME", "RAG PDF Assistant")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # PDF Processing
    MAX_FILE_SIZE_MB = 50
    SUPPORTED_FORMATS = [".pdf", ".docx", ".txt"]
    
    # Chunking Settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # LLM Settings
    DEFAULT_MODEL = "gpt-3.5-turbo"
    EMBEDDING_MODEL = "text-embedding-ada-002"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000
    
    # RAG Settings
    TOP_K_RESULTS = 5
    SIMILARITY_THRESHOLD = 0.7

