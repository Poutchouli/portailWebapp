# Docker Setup for Windows

## Prerequisites

### 1. Install Docker Desktop
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
2. Run the installer and follow the setup wizard
3. Restart your computer when prompted
4. Start Docker Desktop from the Start menu

### 2. Enable WSL 2 (if prompted)
Docker Desktop may require WSL 2 (Windows Subsystem for Linux):
1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart your computer
4. Set WSL 2 as default: `wsl --set-default-version 2`

## Quick Start

### Option 1: Double-click to start
Simply double-click `start.bat` to build and run the application.

### Option 2: Command line
1. Open Command Prompt or PowerShell
2. Navigate to the project folder:
   ```cmd
   cd path\to\local_portal
   ```
3. Run the startup script:
   ```cmd
   start.bat
   ```

### Option 3: Use the helper script
Use `docker.bat` for various operations:
```cmd
docker.bat dev     # Start in development mode
docker.bat start   # Start in background
docker.bat stop    # Stop the application
docker.bat logs    # View logs
docker.bat clean   # Clean up everything
```

## Access Your Application

Once started, access your application at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Stopping the Application

- **From the console**: Press `Ctrl+C`
- **Using script**: Run `docker.bat stop`
- **Docker Desktop**: Use the Docker Desktop interface

## Troubleshooting

### Docker Desktop not starting
- Make sure virtualization is enabled in BIOS
- Check Windows features: Enable "Hyper-V" and "Windows Subsystem for Linux"
- Restart Docker Desktop service

### Port conflicts
If port 8000 is already in use:
1. Edit `docker-compose.yml`
2. Change `"8000:8000"` to `"8080:8000"` (or any other port)
3. Access at http://localhost:8080

### Permission issues
- Run Command Prompt or PowerShell as Administrator
- Make sure your user is in the "docker-users" group

### Build failures
- Make sure you have enough disk space (at least 2GB free)
- Check internet connection for downloading dependencies
- Try running `docker.bat clean` and then `docker.bat build`

## Development on Windows

For development:
1. Use `docker.bat dev` to start with auto-reload
2. Edit `main.py` - changes will trigger automatic restart
3. Database is persisted in the `data\` folder

## File Locations

- **Database**: `data\database.db`
- **Logs**: Use `docker.bat logs` to view
- **Configuration**: `docker-compose.yml`
