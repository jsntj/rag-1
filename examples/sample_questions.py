"""
Sample questions and usage examples for the RAG PDF Assistant
"""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.rag_system import RAGSystem

def sample_usage():
    """Demonstrate basic usage of the RAG system"""
    
    # Initialize components
    print("Initializing RAG system...")
    document_processor = DocumentProcessor()
    vector_store = VectorStore()
    rag_system = RAGSystem(vector_store)
    
    # Sample questions
    sample_questions = [
        "What is the main topic of this document?",
        "Can you summarize the key points?",
        "What are the important dates mentioned?",
        "Who are the main people or organizations discussed?",
        "What are the conclusions or recommendations?",
        "Are there any specific numbers or statistics mentioned?",
        "What problems or challenges are discussed?",
        "What solutions or approaches are proposed?"
    ]
    
    print("\nSample questions you can ask:")
    for i, question in enumerate(sample_questions, 1):
        print(f"{i}. {question}")
    
    print("\nTo use the system:")
    print("1. Upload your PDF documents through the web interface")
    print("2. Ask any of these questions or create your own")
    print("3. The AI will search through your documents and provide answers")

if __name__ == "__main__":
    sample_usage()
