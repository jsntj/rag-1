"""
Main application for the RAG PDF Assistant
"""
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import streamlit as st
from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_system import RAGSystem
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGApplication:
    """Main application class"""
    
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = None
        self.rag_system = None
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize all components"""
        try:
            # Check API key
            if not Config.OPENAI_API_KEY:
                st.error("Please set your OPENAI_API_KEY in the .env file")
                st.stop()
            
            # Initialize vector store
            self.vector_store = VectorStore()
            
            # Initialize RAG system
            self.rag_system = RAGSystem(self.vector_store)
            
            logger.info("All components initialized successfully")
        except Exception as e:
            st.error(f"Error initializing components: {e}")
            st.stop()
    
    def upload_and_process_documents(self, uploaded_files) -> bool:
        """Process uploaded documents"""
        try:
            if not uploaded_files:
                return False
            
            all_chunks = []
            
            for uploaded_file in uploaded_files:
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process document
                chunks = self.document_processor.process_document(temp_path)
                all_chunks.extend(chunks)
                
                # Clean up temp file
                os.remove(temp_path)
            
            # Add to vector store
            if all_chunks:
                success = self.vector_store.add_documents(all_chunks)
                if success:
                    st.success(f"Successfully processed {len(uploaded_files)} documents with {len(all_chunks)} chunks")
                    return True
                else:
                    st.error("Failed to add documents to vector store")
                    return False
            else:
                st.warning("No content extracted from uploaded documents")
                return False
                
        except Exception as e:
            st.error(f"Error processing documents: {e}")
            return False
    
    def process_directory(self, directory_path: str) -> bool:
        """Process all documents in a directory"""
        try:
            if not os.path.exists(directory_path):
                st.error(f"Directory not found: {directory_path}")
                return False
            
            chunks = self.document_processor.process_directory(directory_path)
            
            if chunks:
                success = self.vector_store.add_documents(chunks)
                if success:
                    st.success(f"Successfully processed directory with {len(chunks)} chunks")
                    return True
                else:
                    st.error("Failed to add documents to vector store")
                    return False
            else:
                st.warning("No documents found in directory")
                return False
                
        except Exception as e:
            st.error(f"Error processing directory: {e}")
            return False

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="RAG PDF Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 RAG PDF Assistant")
    st.markdown("Upload PDF documents and ask questions about their content!")
    
    # Initialize application
    if 'rag_app' not in st.session_state:
        st.session_state.rag_app = RAGApplication()
        st.session_state.chat_history = []
    
    rag_app = st.session_state.rag_app
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📄 Document Management")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload one or more PDF, DOCX, or TXT files"
        )
        
        if st.button("Process Documents", type="primary"):
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    success = rag_app.upload_and_process_documents(uploaded_files)
                    if success:
                        st.rerun()
            else:
                st.warning("Please upload some documents first")
        
        # Directory processing
        st.subheader("Or process a directory")
        directory_path = st.text_input("Directory path:", placeholder="/path/to/documents")
        if st.button("Process Directory"):
            if directory_path:
                with st.spinner("Processing directory..."):
                    success = rag_app.process_directory(directory_path)
                    if success:
                        st.rerun()
            else:
                st.warning("Please enter a directory path")
        
        # Database info
        st.subheader("📊 Database Info")
        if rag_app.vector_store:
            info = rag_app.vector_store.get_collection_info()
            st.write(f"Documents: {info.get('document_count', 0)}")
            st.write(f"Collection: {info.get('collection_name', 'N/A')}")
        
        # Clear database
        if st.button("🗑️ Clear Database", type="secondary"):
            rag_app.vector_store.clear_database()
            st.success("Database cleared!")
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat with your documents")
        
        # Chat interface
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = rag_app.rag_system.chat_with_context(
                        prompt, 
                        st.session_state.chat_history
                    )
                    
                    st.markdown(response["answer"])
                    
                    # Show sources if available
                    if response["sources"]:
                        with st.expander("📚 Sources"):
                            for source in response["sources"]:
                                st.write(f"• {source}")
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": response["answer"]})
    
    with col2:
        st.header("🔍 Document Search")
        
        # Search interface
        search_query = st.text_input("Search documents:", placeholder="Enter search terms...")
        if st.button("Search"):
            if search_query:
                with st.spinner("Searching..."):
                    results = rag_app.rag_system.get_context_for_question(search_query)
                    
                    if results:
                        st.write(f"Found {len(results)} relevant sections:")
                        for i, result in enumerate(results):
                            with st.expander(f"Result {i+1} - {result['filename']}"):
                                st.write(result["content"])
                                st.caption(f"Source: {result['source']}")
                    else:
                        st.write("No relevant results found")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("📋 Summarize Documents"):
            if st.session_state.messages:
                summary_prompt = "Please provide a summary of the main topics and key information in the uploaded documents."
                response = rag_app.rag_system.answer_question(summary_prompt)
                st.write("**Document Summary:**")
                st.write(response["answer"])
            else:
                st.warning("Please upload and process some documents first")
        
        if st.button("❓ Sample Questions"):
            sample_questions = [
                "What are the main topics covered in these documents?",
                "Can you summarize the key findings?",
                "What are the important dates mentioned?",
                "Who are the main people or organizations mentioned?",
                "What are the recommendations or conclusions?"
            ]
            st.write("Try asking:")
            for q in sample_questions:
                st.write(f"• {q}")

if __name__ == "__main__":
    main()
