"""
RAG (Retrieval-Augmented Generation) system implementation
"""
import logging
from typing import List, Dict, Any, Optional
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document as LangchainDocument
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGSystem:
    """Main RAG system for question answering"""
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = self._initialize_llm()
        self.qa_chain = self._initialize_qa_chain()
    
    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            llm = ChatOpenAI(
                openai_api_key=Config.OPENAI_API_KEY,
                model_name=Config.DEFAULT_MODEL,
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS
            )
            logger.info(f"Initialized LLM: {Config.DEFAULT_MODEL}")
            return llm
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            raise
    
    def _initialize_qa_chain(self):
        """Initialize the question-answering chain"""
        try:
            # Create a custom prompt template
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

            Context:
            {context}

            Question: {question}

            Answer:"""
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create the QA chain
            qa_chain = load_qa_chain(
                self.llm,
                chain_type="stuff",
                prompt=PROMPT
            )
            
            logger.info("QA chain initialized successfully")
            return qa_chain
        except Exception as e:
            logger.error(f"Error initializing QA chain: {e}")
            raise
    
    def answer_question(self, question: str, use_relevant_docs: bool = True) -> Dict[str, Any]:
        """Answer a question using the RAG system"""
        try:
            if use_relevant_docs:
                # Get relevant documents
                relevant_docs = self.vector_store.get_relevant_documents(question)
                
                if not relevant_docs:
                    return {
                        "answer": "I couldn't find any relevant information in the documents to answer your question.",
                        "sources": [],
                        "confidence": "low"
                    }
                
                # Use QA chain with relevant documents
                result = self.qa_chain({
                    "input_documents": relevant_docs,
                    "question": question
                })
                
                answer = result["output_text"]
                sources = [doc.metadata.get("source", "Unknown") for doc in relevant_docs]
                
                return {
                    "answer": answer,
                    "sources": sources,
                    "confidence": "high" if len(relevant_docs) > 0 else "low"
                }
            else:
                # Direct LLM response without retrieval
                response = self.llm.predict(question)
                return {
                    "answer": response,
                    "sources": [],
                    "confidence": "medium"
                }
                
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                "answer": f"Sorry, I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "confidence": "low"
            }
    
    def get_context_for_question(self, question: str, k: int = None) -> List[Dict[str, Any]]:
        """Get context documents for a question"""
        try:
            relevant_docs = self.vector_store.get_relevant_documents(question, k=k)
            
            context_info = []
            for doc in relevant_docs:
                context_info.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "filename": doc.metadata.get("filename", "Unknown"),
                    "chunk_index": doc.metadata.get("chunk_index", 0)
                })
            
            return context_info
        except Exception as e:
            logger.error(f"Error getting context: {e}")
            return []
    
    def chat_with_context(self, question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Enhanced chat with context from documents and chat history"""
        try:
            # Get relevant documents
            relevant_docs = self.vector_store.get_relevant_documents(question)
            
            # Build context from documents
            context_parts = []
            for doc in relevant_docs:
                context_parts.append(f"Source: {doc.metadata.get('filename', 'Unknown')}\n{doc.page_content}")
            
            context = "\n\n".join(context_parts)
            
            # Build chat history context
            history_context = ""
            if chat_history:
                history_parts = []
                for msg in chat_history[-5:]:  # Last 5 messages
                    history_parts.append(f"{msg['role']}: {msg['content']}")
                history_context = "\n".join(history_parts)
            
            # Create enhanced prompt
            enhanced_prompt = f"""You are a helpful AI assistant that answers questions based on provided documents and chat history.

            Chat History:
            {history_context}

            Document Context:
            {context}

            Question: {question}

            Please provide a helpful answer based on the document context and chat history. If the information isn't available in the documents, say so and provide a general answer if possible."""

            response = self.llm.predict(enhanced_prompt)
            
            return {
                "answer": response,
                "sources": [doc.metadata.get("source", "Unknown") for doc in relevant_docs],
                "confidence": "high" if len(relevant_docs) > 0 else "medium"
            }
            
        except Exception as e:
            logger.error(f"Error in chat with context: {e}")
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "sources": [],
                "confidence": "low"
            }
