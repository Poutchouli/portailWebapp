#!/bin/bash

# Helper script for Docker operations

case "$1" in
    "build")
        echo "Building Docker image..."
        docker-compose build
        ;;
    "start")
        echo "Starting application..."
        docker-compose up -d
        ;;
    "stop")
        echo "Stopping application..."
        docker-compose down
        ;;
    "restart")
        echo "Restarting application..."
        docker-compose down
        docker-compose up -d
        ;;
    "logs")
        echo "Showing logs..."
        docker-compose logs -f app
        ;;
    "shell")
        echo "Opening shell in container..."
        docker-compose exec app /bin/bash
        ;;
    "clean")
        echo "Cleaning up Docker containers and images..."
        docker-compose down --rmi all --volumes --remove-orphans
        ;;
    "dev")
        echo "Starting in development mode with logs..."
        docker-compose up --build
        ;;
    *)
        echo "Usage: $0 {build|start|stop|restart|logs|shell|clean|dev}"
        echo ""
        echo "Commands:"
        echo "  build   - Build the Docker image"
        echo "  start   - Start the application in detached mode"
        echo "  stop    - Stop the application"
        echo "  restart - Restart the application"
        echo "  logs    - Show application logs"
        echo "  shell   - Open a shell in the running container"
        echo "  clean   - Remove all Docker containers and images"
        echo "  dev     - Start in development mode with live logs"
        exit 1
        ;;
esac
