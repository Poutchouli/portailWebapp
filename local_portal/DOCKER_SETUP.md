# Docker Setup Instructions

## Prerequisites

1. **Install Docker:**
   - Ubuntu/Debian: `sudo apt-get install docker.io docker-compose-plugin`
   - Or follow instructions at: https://docs.docker.com/engine/install/

2. **Add your user to docker group (to avoid permission issues):**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```
   Or log out and log back in.

3. **Start Docker service:**
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

## Quick Start

1. **Build and start the application:**
   ```bash
   ./docker.sh dev
   ```

2. **Or use docker-compose directly:**
   ```bash
   docker-compose up --build
   ```

3. **Access your application:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## Useful Commands

- `./docker.sh start` - Start in background
- `./docker.sh stop` - Stop the application
- `./docker.sh logs` - View logs
- `./docker.sh shell` - Open shell in container
- `./docker.sh clean` - Clean up everything

## Troubleshooting

- **Permission denied**: Make sure Docker is installed and your user is in the docker group
- **Port conflicts**: Change port 8000 to another port in docker-compose.yml
- **Build failures**: Make sure all required files are present and Docker has enough space
