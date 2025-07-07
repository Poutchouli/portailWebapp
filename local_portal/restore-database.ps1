# Database Restore Script for Portal Application
# This script restores a backup file to the active database

param(
    [Parameter(Mandatory=$false)]
    [string]$BackupFile
)

Write-Host "=== Portal Database Restore Script ===" -ForegroundColor Green

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

# List available backups if no file specified
if (-not $BackupFile) {
    Write-Host "Available backup files:" -ForegroundColor Cyan
    $backups = Get-ChildItem -Path ".\backups\database_backup_*.db" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    
    if ($backups.Count -eq 0) {
        Write-Host "No backup files found in ./backups directory." -ForegroundColor Red
        exit 1
    }
    
    for ($i = 0; $i -lt $backups.Count; $i++) {
        $size = [math]::Round($backups[$i].Length / 1KB, 2)
        Write-Host "  [$($i+1)] $($backups[$i].Name) ($size KB) - $($backups[$i].LastWriteTime)" -ForegroundColor White
    }
    
    $choice = Read-Host "`nEnter the number of the backup to restore (or 'q' to quit)"
    
    if ($choice -eq 'q' -or $choice -eq 'Q') {
        Write-Host "Restore cancelled." -ForegroundColor Yellow
        exit 0
    }
    
    try {
        $index = [int]$choice - 1
        if ($index -lt 0 -or $index -ge $backups.Count) {
            throw "Invalid selection"
        }
        $BackupFile = $backups[$index].Name
    } catch {
        Write-Host "Invalid selection. Exiting." -ForegroundColor Red
        exit 1
    }
}

# Verify backup file exists
$backupPath = ".\backups\$BackupFile"
if (!(Test-Path $backupPath)) {
    Write-Host "Error: Backup file '$BackupFile' not found in ./backups directory." -ForegroundColor Red
    exit 1
}

Write-Host "`nSelected backup: $BackupFile" -ForegroundColor Cyan

# Confirm restore operation
$confirm = Read-Host "This will REPLACE your current database. Are you sure? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Restore cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host "`n=== Starting Restore Process ===" -ForegroundColor Yellow

# Step 1: Stop the app service
Write-Host "Step 1: Stopping app service..." -ForegroundColor Yellow
docker-compose stop app

# Step 2: Backup current database (safety measure)
if (Test-Path ".\data\database.db") {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $safetyBackup = ".\backups\pre_restore_backup_$timestamp.db"
    Write-Host "Step 2: Creating safety backup of current database..." -ForegroundColor Yellow
    Copy-Item ".\data\database.db" $safetyBackup
    Write-Host "Safety backup created: $safetyBackup" -ForegroundColor Green
}

# Step 3: Restore the backup
Write-Host "Step 3: Restoring backup file..." -ForegroundColor Yellow
Copy-Item $backupPath ".\data\database.db" -Force

# Step 4: Start the app service
Write-Host "Step 4: Starting app service..." -ForegroundColor Yellow
docker-compose start app

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Restore Complete ===" -ForegroundColor Green
    Write-Host "Database has been restored from: $BackupFile" -ForegroundColor Cyan
    Write-Host "Your application should be running again on http://localhost:8000" -ForegroundColor Cyan
} else {
    Write-Host "`nError: Failed to start app service after restore." -ForegroundColor Red
    Write-Host "You may need to run 'docker-compose start app' manually." -ForegroundColor Yellow
}
