# Backup Cleanup Script
# This script helps manage backup files by removing old backups

param(
    [Parameter(Mandatory=$false)]
    [int]$KeepLast = 10
)

Write-Host "=== Backup Cleanup Script ===" -ForegroundColor Green
Write-Host "This script will keep the $KeepLast most recent backups and delete the rest." -ForegroundColor Yellow

# Check if backups directory exists
if (!(Test-Path ".\backups")) {
    Write-Host "Backups directory not found." -ForegroundColor Red
    exit 1
}

# Get all backup files
$backups = Get-ChildItem -Path ".\backups\database_backup_*.db" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending

if ($backups.Count -eq 0) {
    Write-Host "No backup files found." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($backups.Count) backup files." -ForegroundColor Cyan

if ($backups.Count -le $KeepLast) {
    Write-Host "All backup files will be kept (found $($backups.Count), keeping $KeepLast)." -ForegroundColor Green
    exit 0
}

# Show files that will be kept
Write-Host "`nBackup files to KEEP (most recent $KeepLast):" -ForegroundColor Green
$toKeep = $backups | Select-Object -First $KeepLast
foreach ($backup in $toKeep) {
    $size = [math]::Round($backup.Length / 1KB, 2)
    Write-Host "  ✓ $($backup.Name) ($size KB) - $($backup.LastWriteTime)" -ForegroundColor Green
}

# Show files that will be deleted
Write-Host "`nBackup files to DELETE:" -ForegroundColor Red
$toDelete = $backups | Select-Object -Skip $KeepLast
foreach ($backup in $toDelete) {
    $size = [math]::Round($backup.Length / 1KB, 2)
    Write-Host "  ✗ $($backup.Name) ($size KB) - $($backup.LastWriteTime)" -ForegroundColor Red
}

# Calculate space to be freed
$spaceToFree = ($toDelete | Measure-Object -Property Length -Sum).Sum
$spaceToFreeKB = [math]::Round($spaceToFree / 1KB, 2)

Write-Host "`nThis will free up $spaceToFreeKB KB of disk space." -ForegroundColor Cyan

# Confirm deletion
$confirm = Read-Host "`nProceed with deletion? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    exit 0
}

# Delete old backups
Write-Host "`nDeleting old backup files..." -ForegroundColor Yellow
$deletedCount = 0
foreach ($backup in $toDelete) {
    try {
        Remove-Item $backup.FullName -Force
        Write-Host "  Deleted: $($backup.Name)" -ForegroundColor Gray
        $deletedCount++
    } catch {
        Write-Host "  Failed to delete: $($backup.Name) - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== Cleanup Complete ===" -ForegroundColor Green
Write-Host "Deleted $deletedCount backup files." -ForegroundColor Cyan
Write-Host "Kept $($toKeep.Count) most recent backup files." -ForegroundColor Cyan

# Show remaining files
Write-Host "`nRemaining backup files:" -ForegroundColor Cyan
$remaining = Get-ChildItem -Path ".\backups\database_backup_*.db" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending
foreach ($backup in $remaining) {
    $size = [math]::Round($backup.Length / 1KB, 2)
    Write-Host "  $($backup.Name) ($size KB) - $($backup.LastWriteTime)" -ForegroundColor White
}
