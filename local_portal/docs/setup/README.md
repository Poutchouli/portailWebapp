# Setup Documentation

This directory contains platform-specific setup and configuration documentation for the portal application.

## Files

### Platform Setup Guides
- **`WINDOWS_SETUP.md`** - Complete setup guide for Windows users including Docker Desktop installation
- **`DOCKER_SETUP.md`** - Docker setup instructions for Linux systems

## Quick Start

### Windows Users
1. Follow `WINDOWS_SETUP.md` to install Docker Desktop
2. Use `../../start.bat` or `../../docker.bat` for easy startup
3. Access the app at http://localhost:8000

### Linux Users
1. Follow `DOCKER_SETUP.md` to install Docker and Docker Compose
2. Use `../../docker.sh` for startup and management
3. Access the app at http://localhost:8000

## Key Features Covered

### Windows Setup
- Docker Desktop installation
- WSL 2 configuration
- Batch script usage (`start.bat`, `docker.bat`)
- PowerShell troubleshooting

### Linux Setup  
- Docker engine installation
- User permissions configuration
- Shell script usage (`docker.sh`)
- Common troubleshooting

## Related Files
- Startup scripts: `../../start.bat`, `../../docker.bat`, `../../docker.sh`
- Docker configuration: `../../docker-compose.yml`, `../../Dockerfile`
- Build scripts: `../../build-and-run.bat`
