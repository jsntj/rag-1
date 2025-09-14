@echo off
echo Installing RAG PDF Assistant...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    copy env.example .env
    echo Created .env file from template
    echo Please edit .env and add your OpenAI API key
)

echo.
echo Installation complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: streamlit run app.py
echo.
pause
