@echo off
REM Helper script for Docker operations on Windows

if "%1"=="build" (
    echo Building Docker image...
    docker-compose build
    goto :eof
)

if "%1"=="start" (
    echo Starting application...
    docker-compose up -d
    goto :eof
)

if "%1"=="stop" (
    echo Stopping application...
    docker-compose down
    goto :eof
)

if "%1"=="restart" (
    echo Restarting application...
    docker-compose down
    docker-compose up -d
    goto :eof
)

if "%1"=="logs" (
    echo Showing recent logs...
    docker-compose logs --tail=50 app
    goto :eof
)

if "%1"=="shell" (
    echo Opening shell in container...
    docker-compose exec app /bin/bash
    goto :eof
)

if "%1"=="follow" (
    echo Following logs in real-time (Press Ctrl+C to stop)...
    docker-compose logs -f app
    goto :eof
)

if "%1"=="clean" (
    echo Cleaning up Docker containers and images...
    docker-compose down --rmi all --volumes --remove-orphans
    goto :eof
)

if "%1"=="dev" (
    echo Starting in development mode with logs...
    docker-compose up --build
    goto :eof
)

REM Default case - show usage
echo Usage: %0 {build^|start^|stop^|restart^|logs^|follow^|shell^|clean^|dev}
echo.
echo Commands:
echo   build   - Build the Docker image
echo   start   - Start the application in detached mode
echo   stop    - Stop the application
echo   restart - Restart the application
echo   logs    - Show recent application logs (last 50 lines)
echo   follow  - Follow application logs in real-time (Ctrl+C to stop)
echo   shell   - Open a shell in the running container
echo   clean   - Remove all Docker containers and images
echo   dev     - Start in development mode with live logs
