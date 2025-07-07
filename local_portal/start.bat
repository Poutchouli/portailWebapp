@echo off
echo ====================================
echo    Local Portal Backend Startup
echo ====================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running
    echo Please start Docker Desktop and try again
    echo.
    pause
    exit /b 1
)

echo Docker is installed and running!
echo.

REM Navigate to the script directory
cd /d "%~dp0"

echo Building and starting the Local Portal Backend...
echo This may take a few minutes on the first run.
echo.

REM Build and start the application
docker-compose up --build

echo.
echo Application stopped. Press any key to exit...
pause >nul
