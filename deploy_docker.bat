@echo off
echo Deploying FastAPI with Docker Compose...

REM Check if Docker is running
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Docker is not running or not installed. Please start Docker Desktop first.
    exit /b 1
)

REM Check if port 8000 is in use
echo Checking port availability...
netstat -ano | findstr :8000 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Port 8000 is already in use. Using alternative port...
    set API_PORT=8080
) else (
    set API_PORT=8000
)

echo Setting API_PORT=%API_PORT%

REM Build and start the services
echo Building and starting services...
docker-compose down
docker-compose build
docker-compose up -d

echo.
if %ERRORLEVEL% EQU 0 (
    echo Deployment successful!
    echo API is now available at http://localhost:%API_PORT%
    echo API documentation at http://localhost:%API_PORT%/docs
) else (
    echo Deployment failed. Please check the logs.
) 