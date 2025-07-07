# Scripts Directory

This directory contains all utility scripts for the Local WebApp Portal project, organized by platform and functionality.

## Directory Structure

```
scripts/
├── windows/              # Windows PowerShell scripts
│   ├── backup-database.ps1     # Safe backup (stops service)
│   ├── quick-backup.ps1        # Quick backup (service running)
│   ├── restore-database.ps1    # Interactive restore
│   ├── cleanup-backups.ps1     # Cleanup old backups
│   └── backup-manager.ps1      # Menu-driven interface
├── linux/                # Linux/macOS Bash scripts
│   ├── backup_db.sh            # Safe backup (stops service)
│   ├── quick_backup.sh         # Quick backup (service running)
│   ├── restore_db.sh           # Interactive restore
│   ├── cleanup_backups.sh      # Cleanup old backups
│   ├── backup_manager.sh       # Menu-driven interface
│   └── setup_cron.sh           # Automated scheduling
└── test_api.sh            # API testing script (cross-platform)
```

## Quick Usage

### Windows (PowerShell)
```powershell
# Navigate to project root
cd path\to\local_portal

# Quick backup
.\scripts\windows\quick-backup.ps1

# Safe backup
.\scripts\windows\backup-database.ps1

# Interactive management
.\scripts\windows\backup-manager.ps1
```

### Linux/macOS (Bash)
```bash
# Navigate to project root
cd /path/to/local_portal

# Make scripts executable (first time only)
chmod +x scripts/linux/*.sh

# Quick backup
./scripts/linux/quick_backup.sh

# Safe backup
./scripts/linux/backup_db.sh

# Interactive management
./scripts/linux/backup_manager.sh

# Set up automated backups
./scripts/linux/setup_cron.sh daily
```

## Script Descriptions

### Backup Scripts

**Safe Backup Scripts** (`backup-database.ps1` / `backup_db.sh`):
- Stop the application service
- Create timestamped backup
- Restart the application service
- Comprehensive logging
- Recommended for production

**Quick Backup Scripts** (`quick-backup.ps1` / `quick_backup.sh`):
- Create backup without stopping service
- Faster execution
- Suitable for development
- Small risk of inconsistency during active writes

**Restore Scripts** (`restore-database.ps1` / `restore_db.sh`):
- Interactive backup selection
- Safety backup before restore
- Service management
- Confirmation prompts

**Cleanup Scripts** (`cleanup-backups.ps1` / `cleanup_backups.sh`):
- Remove old backup files
- Keep N most recent backups
- Calculate space savings
- Confirmation prompts

**Management Scripts** (`backup-manager.ps1` / `backup_manager.sh`):
- Menu-driven interface
- All backup operations in one place
- Backup statistics
- Log viewing

### Platform-Specific Features

**Linux-Only**:
- `setup_cron.sh` - Automated scheduling with cron jobs

**Cross-Platform**:
- `test_api.sh` - API testing script (works on Windows with Git Bash)

## Important Notes

### Path Updates Required

Since scripts have been moved to subdirectories, you need to update the paths when calling them:

**Before** (when in project root):
```bash
./quick-backup.ps1
```

**After** (when in project root):
```bash
./scripts/windows/quick-backup.ps1
```

### Docker Compose Context

All scripts assume they are run from the project root directory (where `docker-compose.yml` is located). The scripts will automatically adjust their working directory as needed.

### Documentation

For detailed usage instructions, see:
- Windows: `docs/backup/BACKUP_README.md`
- Linux: `docs/backup/LINUX_BACKUP_README.md`
- Complete guide: `docs/backup/CROSS_PLATFORM_BACKUP_SUMMARY.md`
