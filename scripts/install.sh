#!/bin/bash

echo "Installing RAG PDF Assistant..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp env.example .env
    echo "Created .env file from template"
    echo "Please edit .env and add your OpenAI API key"
fi

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: streamlit run app.py"
echo ""
