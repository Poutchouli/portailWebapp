# Comprehensive Backup Management Script
# This script provides a menu-driven interface for all backup operations

function Show-Menu {
    Clear-Host
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host "    DATABASE BACKUP MANAGEMENT        " -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Create Safe Backup (stops service)" -ForegroundColor Green
    Write-Host "2. Create Quick Backup (service running)" -ForegroundColor Yellow
    Write-Host "3. List Backup Files" -ForegroundColor Cyan
    Write-Host "4. Restore Database" -ForegroundColor Magenta
    Write-Host "5. Cleanup Old Backups" -ForegroundColor Red
    Write-Host "6. View Backup Statistics" -ForegroundColor White
    Write-Host "0. Exit" -ForegroundColor Gray
    Write-Host ""
}

function Get-BackupStats {
    $backups = Get-ChildItem -Path ".\backups\database_backup_*.db" -ErrorAction SilentlyContinue
    
    if ($backups.Count -eq 0) {
        Write-Host "No backup files found." -ForegroundColor Yellow
        return
    }
    
    $totalSize = ($backups | Measure-Object -Property Length -Sum).Sum
    $totalSizeKB = [math]::Round($totalSize / 1KB, 2)
    $totalSizeMB = [math]::Round($totalSize / 1MB, 2)
    
    $oldest = $backups | Sort-Object LastWriteTime | Select-Object -First 1
    $newest = $backups | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    Write-Host "=== Backup Statistics ===" -ForegroundColor Cyan
    Write-Host "Total backup files: $($backups.Count)" -ForegroundColor White
    Write-Host "Total space used: $totalSizeKB KB ($totalSizeMB MB)" -ForegroundColor White
    Write-Host "Oldest backup: $($oldest.Name) ($($oldest.LastWriteTime))" -ForegroundColor White
    Write-Host "Newest backup: $($newest.Name) ($($newest.LastWriteTime))" -ForegroundColor White
    
    # Calculate average backup size
    $avgSize = [math]::Round($totalSize / $backups.Count / 1KB, 2)
    Write-Host "Average backup size: $avgSize KB" -ForegroundColor White
}

function Show-Backups {
    Write-Host "=== Available Backup Files ===" -ForegroundColor Cyan
    $backups = Get-ChildItem -Path ".\backups\database_backup_*.db" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
    
    if ($backups.Count -eq 0) {
        Write-Host "No backup files found." -ForegroundColor Yellow
        return
    }
    
    for ($i = 0; $i -lt $backups.Count; $i++) {
        $size = [math]::Round($backups[$i].Length / 1KB, 2)
        $age = (Get-Date) - $backups[$i].LastWriteTime
        $ageText = if ($age.TotalDays -ge 1) { "$([math]::Floor($age.TotalDays)) days ago" } 
                   elseif ($age.TotalHours -ge 1) { "$([math]::Floor($age.TotalHours)) hours ago" }
                   else { "$([math]::Floor($age.TotalMinutes)) minutes ago" }
        
        Write-Host "  [$($i+1)] $($backups[$i].Name)" -ForegroundColor White
        Write-Host "      Size: $size KB | Created: $ageText | Date: $($backups[$i].LastWriteTime)" -ForegroundColor Gray
    }
}

# Check prerequisites
if (!(Test-Path "docker-compose.yml")) {
    Write-Host "Error: docker-compose.yml not found. Please run this script from the local_portal directory." -ForegroundColor Red
    exit 1
}

try {
    docker version | Out-Null
} catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Create backups directory if it doesn't exist
if (!(Test-Path ".\backups")) {
    New-Item -ItemType Directory -Path ".\backups" | Out-Null
}

# Main menu loop
do {
    Show-Menu
    $choice = Read-Host "Select an option (0-6)"
    
    switch ($choice) {
        "1" {
            Write-Host "`nExecuting safe backup..." -ForegroundColor Yellow
            .\backup-database.ps1
            Write-Host "`nPress any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "2" {
            Write-Host "`nExecuting quick backup..." -ForegroundColor Yellow
            .\quick-backup.ps1
            Write-Host "`nPress any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "3" {
            Clear-Host
            Show-Backups
            Write-Host "`nPress any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "4" {
            Write-Host "`nExecuting database restore..." -ForegroundColor Yellow
            .\restore-database.ps1
            Write-Host "`nPress any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "5" {
            Write-Host "`nExecuting backup cleanup..." -ForegroundColor Yellow
            .\cleanup-backups.ps1
            Write-Host "`nPress any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "6" {
            Clear-Host
            Get-BackupStats
            Write-Host "`nPress any key to continue..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "0" {
            Write-Host "Goodbye!" -ForegroundColor Green
        }
        default {
            Write-Host "Invalid option. Please try again." -ForegroundColor Red
            Start-Sleep 2
        }
    }
} while ($choice -ne "0")
