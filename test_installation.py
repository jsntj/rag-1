"""
Test script to verify the RAG PDF Assistant installation
"""
import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    try:
        import streamlit
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import langchain
        print("✓ LangChain imported successfully")
    except ImportError as e:
        print(f"✗ LangChain import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✓ ChromaDB imported successfully")
    except ImportError as e:
        print(f"✗ ChromaDB import failed: {e}")
        return False
    
    try:
        import openai
        print("✓ OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✓ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"✗ PyPDF2 import failed: {e}")
        return False
    
    try:
        import fitz
        print("✓ PyMuPDF imported successfully")
    except ImportError as e:
        print(f"✗ PyMuPDF import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config import Config
        print("✓ Configuration loaded successfully")
        
        # Check if API key is set
        if Config.OPENAI_API_KEY:
            print("✓ OpenAI API key is configured")
        else:
            print("⚠ OpenAI API key not set (add to .env file)")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_components():
    """Test core components initialization"""
    print("\nTesting component initialization...")
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        print("✓ Document processor initialized")
        
        # Only test vector store if API key is available
        from config import Config
        if Config.OPENAI_API_KEY:
            from vector_store import VectorStore
            vector_store = VectorStore()
            print("✓ Vector store initialized")
            
            from rag_system import RAGSystem
            rag_system = RAGSystem(vector_store)
            print("✓ RAG system initialized")
        else:
            print("⚠ Skipping vector store and RAG system tests (no API key)")
        
        return True
    except Exception as e:
        print(f"✗ Component initialization failed: {e}")
        return False

def main():
    """Run all tests"""
    print("RAG PDF Assistant - Installation Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test configuration
    if not test_config():
        all_passed = False
    
    # Test components
    if not test_components():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed! Installation is successful.")
        print("\nNext steps:")
        print("1. Add your OpenAI API key to the .env file")
        print("2. Run: streamlit run app.py")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that you're using Python 3.8 or higher")
        print("3. Verify your .env file is properly configured")

if __name__ == "__main__":
    main()
