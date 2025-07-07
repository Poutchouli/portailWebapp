# Database Backup Script for Portal Application
# This script safely backs up the SQLite database by temporarily stopping the app service

Write-Host "=== Portal Database Backup Script ===" -ForegroundColor Green
Write-Host "Starting backup process..." -ForegroundColor Yellow

# Check if Docker is running
try {
    docker version | Out-Null
} catch {
    Write-Host "Error: Docker is not running or not accessible. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if we're in the correct directory
if (!(Test-Path "docker-compose.yml")) {
    Write-Host "Error: docker-compose.yml not found. Please run this script from the local_portal directory." -ForegroundColor Red
    exit 1
}

# Step 1: Stop the app service for consistent backup
Write-Host "Step 1: Stopping app service for consistent backup..." -ForegroundColor Yellow
docker-compose stop app

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Failed to stop app service. Continuing with backup anyway..." -ForegroundColor Yellow
}

# Step 2: Run the backup
Write-Host "Step 2: Creating database backup..." -ForegroundColor Yellow
docker-compose run --rm backup-db

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Backup failed!" -ForegroundColor Red
    Write-Host "Step 3: Restarting app service..." -ForegroundColor Yellow
    docker-compose start app
    exit 1
}

# Step 3: Restart the app service
Write-Host "Step 3: Restarting app service..." -ForegroundColor Yellow
docker-compose start app

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Failed to restart app service. You may need to run 'docker-compose start app' manually." -ForegroundColor Yellow
}

Write-Host "=== Backup Process Complete ===" -ForegroundColor Green
Write-Host "Check the ./backups directory for your backup file." -ForegroundColor Cyan

# List recent backups
Write-Host "`nRecent backup files:" -ForegroundColor Cyan
Get-ChildItem -Path ".\backups\database_backup_*.db" | Sort-Object LastWriteTime -Descending | Select-Object -First 5 | ForEach-Object {
    $size = [math]::Round($_.Length / 1KB, 2)
    Write-Host "  $($_.Name) ($size KB) - $($_.LastWriteTime)" -ForegroundColor White
}
