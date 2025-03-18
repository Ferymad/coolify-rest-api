@echo off
echo Setting up development environment...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Development environment setup complete!
echo To start the application, run: python run_dev.py
echo Or run: uvicorn main:app --reload
echo. 