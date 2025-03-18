@echo off
echo Testing the FastAPI API...

REM Activate virtual environment if it exists
if exist venv (
    call venv\Scripts\activate
)

REM Check if requests library is installed
pip show requests > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing requests library...
    pip install requests
)

REM Run the test script
python test_api.py %*

REM Deactivate virtual environment if it was activated
if exist venv (
    call deactivate
) 