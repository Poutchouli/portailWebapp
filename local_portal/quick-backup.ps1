# Quick Database Backup Script (without stopping service)
# Use this for quick backups when the database is not heavily in use

Write-Host "=== Quick Portal Database Backup ===" -ForegroundColor Green

# Check if Docker is running
try {
    docker version | Out-Null
} catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if we're in the correct directory
if (!(Test-Path "docker-compose.yml")) {
    Write-Host "Error: docker-compose.yml not found. Please run this script from the local_portal directory." -ForegroundColor Red
    exit 1
}

Write-Host "Creating quick backup (service will continue running)..." -ForegroundColor Yellow
docker-compose run --rm backup-db

if ($LASTEXITCODE -eq 0) {
    Write-Host "Quick backup completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Backup failed!" -ForegroundColor Red
    exit 1
}
