# Database Backup System

This directory contains a dockerized backup solution for your SQLite database. The backup system is integrated into your Docker Compose setup and provides several convenient scripts for managing backups.

## Quick Start

### Creating a Backup

**Safe backup (recommended):**
```powershell
.\backup-database.ps1
```
This stops the app service, creates the backup, then restarts the service.

**Quick backup (while service is running):**
```powershell
.\quick-backup.ps1
```
This creates a backup without stopping the service. Use when the database is not heavily in use.

**Manual backup using Docker Compose:**
```powershell
docker-compose run --rm backup-db
```

### Restoring a Backup

```powershell
.\restore-database.ps1
```
This script will:
1. Show you available backup files
2. Let you select which one to restore
3. Create a safety backup of your current database
4. Restore the selected backup
5. Restart your services

## How It Works

### Docker Compose Service

The `backup-db` service in `docker-compose.yml` is configured to:
- Use Alpine Linux (lightweight)
- Mount your `./data` directory (where `database.db` lives)
- Mount a `./backups` directory to store backup files
- Create timestamped backup files with format: `database_backup_YYYYMMDD_HHMMSS.db`

### Backup Files

Backup files are stored in the `./backups` directory with timestamps:
- `database_backup_20250107_143022.db`
- `database_backup_20250107_150500.db`
- etc.

## Advanced Usage

### Scheduling Automated Backups

You can use Windows Task Scheduler to run backups automatically:

1. Open Windows Task Scheduler
2. Create a new task
3. Set it to run `powershell.exe` with arguments:
   ```
   -ExecutionPolicy Bypass -File "F:\WORKWORK\FULL\portailWebapp\local_portal\backup-database.ps1"
   ```
4. Schedule it to run daily, weekly, etc.

### Manual Docker Commands

**Create backup manually:**
```powershell
# Stop service for consistency
docker-compose stop app

# Run backup
docker-compose run --rm backup-db

# Restart service
docker-compose start app
```

**List all services:**
```powershell
docker-compose ps
```

### Backup File Management

**List backup files by date:**
```powershell
Get-ChildItem .\backups\database_backup_*.db | Sort-Object LastWriteTime -Descending
```

**Delete old backups (keep last 10):**
```powershell
Get-ChildItem .\backups\database_backup_*.db | Sort-Object LastWriteTime -Descending | Select-Object -Skip 10 | Remove-Item
```

## Important Notes

### SQLite Backup Consistency

- **Safe approach**: Stop the app service before backup (recommended for production)
- **Quick approach**: Backup while running (acceptable for development, but small risk of inconsistency)

### Storage Considerations

- Backup files accumulate over time
- Monitor disk space in the `./backups` directory
- Consider implementing a cleanup policy for old backups

### Security

- Backup files contain all your user data and should be protected
- Consider encrypting backup files for sensitive environments
- Be cautious when sharing or moving backup files

## Troubleshooting

**"Docker is not running" error:**
- Make sure Docker Desktop is started
- Verify you can run `docker version` in PowerShell

**"docker-compose.yml not found" error:**
- Make sure you're running scripts from the `local_portal` directory
- Verify the `docker-compose.yml` file exists

**Backup fails:**
- Check if the `./data/database.db` file exists
- Verify Docker services are running: `docker-compose ps`
- Check Docker logs: `docker-compose logs app`

**Restore fails:**
- Ensure the backup file exists in `./backups`
- Verify you have write permissions to the `./data` directory
- Check that Docker services can be stopped/started

## File Structure

```
local_portal/
├── docker-compose.yml          # Contains backup-db service
├── backup-database.ps1         # Safe backup script (stops service)
├── quick-backup.ps1           # Quick backup script (service running)
├── restore-database.ps1       # Interactive restore script
├── data/
│   └── database.db           # Your main database file
└── backups/                  # Backup files directory
    ├── database_backup_20250107_143022.db
    ├── database_backup_20250107_150500.db
    └── ...
```
