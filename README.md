# RAG PDF Assistant

A powerful Retrieval-Augmented Generation (RAG) system that allows you to upload PDF documents and ask questions about their content using AI. Built with LangChain, ChromaDB, and Streamlit.

## Features

- 📄 **Multi-format Support**: Process PDF, DOCX, and TXT files
- 🔍 **Intelligent Search**: Semantic search through document content
- 💬 **Interactive Chat**: Ask questions and get contextual answers
- 🧠 **AI-Powered**: Uses OpenAI's GPT models for intelligent responses
- 📊 **Vector Database**: Efficient document storage and retrieval with ChromaDB
- 🎨 **Modern UI**: Clean, intuitive Streamlit interface

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd rag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file and add your API key:

```bash
copy env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## Usage

### Uploading Documents

1. Use the sidebar to upload PDF, DOCX, or TXT files
2. Click "Process Documents" to add them to the knowledge base
3. Documents are automatically chunked and embedded for efficient search

### Asking Questions

1. Type your question in the chat interface
2. The system will search through your documents for relevant information
3. Get AI-powered answers based on the document content

### Document Search

1. Use the search box to find specific information
2. View relevant document sections with source citations
3. Explore different parts of your documents

## Configuration

Edit `config.py` to customize:

- **Chunk Size**: Adjust `CHUNK_SIZE` for document splitting
- **Model Settings**: Change `DEFAULT_MODEL` and `TEMPERATURE`
- **Search Parameters**: Modify `TOP_K_RESULTS` and `SIMILARITY_THRESHOLD`
- **File Limits**: Update `MAX_FILE_SIZE_MB` and `SUPPORTED_FORMATS`

## Project Structure

```
rag/
├── src/
│   ├── __init__.py
│   ├── document_processor.py    # PDF/document processing
│   ├── vector_store.py          # ChromaDB vector operations
│   ├── rag_system.py           # RAG query system
│   └── main.py                 # Streamlit app logic
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── env.example                 # Environment variables template
└── README.md                   # This file
```

## Dependencies

- **LangChain**: Framework for LLM applications
- **ChromaDB**: Vector database for embeddings
- **Streamlit**: Web application framework
- **OpenAI**: Language model API
- **PyPDF2/PyMuPDF**: PDF processing
- **python-docx**: DOCX file processing

## Advanced Usage

### Processing Large Document Collections

For processing many documents, you can use the directory processing feature:

1. Place all your documents in a folder
2. Enter the folder path in the sidebar
3. Click "Process Directory" to process all supported files

### Customizing the AI Responses

Modify the prompt templates in `src/rag_system.py` to customize how the AI responds to questions.

### Adding New Document Types

Extend `src/document_processor.py` to support additional file formats by adding new loader methods.

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your OpenAI API key is correctly set in the `.env` file
2. **Memory Issues**: For large documents, consider reducing `CHUNK_SIZE` in `config.py`
3. **Slow Processing**: Large PDFs may take time to process; this is normal

### Getting Help

- Check the logs in the terminal for detailed error messages
- Ensure all dependencies are installed correctly
- Verify your OpenAI API key has sufficient credits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Vector storage powered by [ChromaDB](https://www.trychroma.com/)
- UI created with [Streamlit](https://streamlit.io/)
- AI capabilities from [OpenAI](https://openai.com/)
