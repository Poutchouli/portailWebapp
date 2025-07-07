# Linux Database Backup System

This documentation covers the Linux shell scripts for managing database backups in your portal application. These scripts complement the Windows PowerShell scripts and provide the same functionality on Linux systems.

## 📁 Linux Backup Scripts

### Core Scripts

1. **`backup_db.sh`** - Safe backup with service stop/start
2. **`quick_backup.sh`** - Quick backup without stopping service  
3. **`restore_db.sh`** - Interactive database restore
4. **`cleanup_backups.sh`** - Clean up old backup files
5. **`backup_manager.sh`** - Menu-driven backup management
6. **`setup_cron.sh`** - Automated scheduling with cron

## 🚀 Quick Start

### Make Scripts Executable
```bash
chmod +x scripts/linux/*.sh
```

### Create a Backup
```bash
# Safe backup (recommended)
./scripts/linux/backup_db.sh

# Quick backup (service keeps running)
./scripts/linux/quick_backup.sh

# Interactive menu
./scripts/linux/backup_manager.sh
```

### Automated Scheduling
```bash
# Set up daily backups at 3 AM
./scripts/linux/setup_cron.sh daily

# Set up weekly backups on Sunday at 2:30 AM
./scripts/linux/setup_cron.sh weekly

# Custom schedule
./scripts/linux/setup_cron.sh custom
```

## 📋 Detailed Script Documentation

### backup_db.sh
**Purpose**: Creates a consistent database backup by stopping the service temporarily.

**Features**:
- Stops app service for consistency
- Creates timestamped backup files
- Comprehensive logging to `backup_log.txt`
- Error handling and service restart
- Backup verification
- Summary statistics

**Usage**:
```bash
./scripts/linux/backup_db.sh
```

**Output**:
- Backup file: `./backups/database_backup_YYYYMMDD_HHMMSS.db`
- Log file: `./backup_log.txt`

### quick_backup.sh  
**Purpose**: Creates a backup without stopping the service (development use).

**Features**:
- No service interruption
- Fast execution
- Basic logging
- Backup verification

**Usage**:
```bash
./scripts/linux/quick_backup.sh
```

### restore_db.sh
**Purpose**: Restores a backup file to the active database.

**Features**:
- Interactive backup selection
- Safety backup before restore
- Service management
- Confirmation prompts
- Command-line backup specification

**Usage**:
```bash
# Interactive selection
./scripts/linux/restore_db.sh

# Specify backup file
./scripts/linux/restore_db.sh database_backup_20250107_143022.db
```

### cleanup_backups.sh
**Purpose**: Manages backup file retention.

**Features**:
- Keeps N most recent backups
- Shows files to be deleted
- Calculates space savings
- Confirmation prompts
- Detailed size reporting

**Usage**:
```bash
# Keep last 10 backups (default)
./scripts/linux/cleanup_backups.sh

# Keep last 5 backups
./scripts/linux/cleanup_backups.sh 5
```

### backup_manager.sh
**Purpose**: Menu-driven interface for all backup operations.

**Features**:
- Interactive menu system
- All operations in one place
- Backup statistics
- Log viewing
- Prerequisite checking

**Usage**:
```bash
./scripts/linux/backup_manager.sh
```

**Menu Options**:
1. Create Safe Backup
2. Create Quick Backup  
3. List Backup Files
4. Restore Database
5. Cleanup Old Backups
6. View Backup Statistics
7. View Recent Logs
0. Exit

### setup_cron.sh
**Purpose**: Automates backup scheduling using cron.

**Features**:
- Predefined schedules (daily, weekly, every 6 hours)
- Custom schedule support
- Cron job management
- List existing jobs
- Remove backup jobs

**Usage**:
```bash
# Set up daily backups
./scripts/linux/setup_cron.sh daily

# Set up weekly backups  
./scripts/linux/setup_cron.sh weekly

# Every 6 hours
./scripts/linux/setup_cron.sh hourly6

# Custom schedule
./scripts/linux/setup_cron.sh custom

# List current jobs
./scripts/linux/setup_cron.sh list

# Remove backup job
./scripts/linux/setup_cron.sh remove
```

## 🔧 Cron Schedule Examples

### Common Schedules
```bash
# Daily at 3:00 AM
0 3 * * *

# Weekly on Sunday at 2:30 AM  
30 2 * * SUN

# Every 6 hours
0 */6 * * *

# Every day at midnight
0 0 * * *

# Monday to Friday at 6:00 AM
0 6 * * 1-5

# First day of month at 1:00 AM
0 1 1 * *
```

### Cron Field Format
```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0 and 7 = Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

## 📁 File Structure

```
local_portal/
├── backup_db.sh              # Safe backup script
├── quick_backup.sh           # Quick backup script  
├── restore_db.sh             # Restore script
├── cleanup_backups.sh        # Cleanup script
├── backup_manager.sh         # Menu interface
├── setup_cron.sh             # Cron setup helper
├── backup_log.txt            # Log file (created automatically)
├── docker-compose.yml        # Contains backup-db service
├── data/
│   └── database.db          # Main database file
└── backups/                 # Backup files directory
    ├── database_backup_20250107_143022.db
    ├── database_backup_20250107_150500.db
    └── ...
```

## 🛡️ Security and Permissions

### Script Permissions
```bash
# Make all scripts executable
chmod +x *.sh

# Specific permissions
chmod 755 backup_db.sh
chmod 755 quick_backup.sh
chmod 755 restore_db.sh
chmod 755 cleanup_backups.sh
chmod 755 backup_manager.sh
chmod 755 setup_cron.sh
```

### Directory Permissions
```bash
# Ensure backup directory is writable
chmod 755 backups/

# Protect log file
chmod 644 backup_log.txt
```

## 🔍 Troubleshooting

### Common Issues

**"Docker is not installed or not in PATH"**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
```

**"Docker daemon is not running"**
```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker on boot
sudo systemctl enable docker
```

**"Permission denied" when running scripts**
```bash
# Make scripts executable
chmod +x *.sh
```

**"docker-compose.yml not found"**
```bash
# Verify you're in the correct directory
pwd
ls -la docker-compose.yml
```

**Backup fails with "database locked"**
```bash
# Use safe backup instead of quick backup
./scripts/linux/backup_db.sh
```

### Log Analysis
```bash
# View recent logs
tail -f backup_log.txt

# Search for errors
grep ERROR backup_log.txt

# View logs from specific date
grep "2025-01-07" backup_log.txt
```

### Manual Recovery
```bash
# Check Docker status
docker compose ps

# Restart services
docker compose restart

# View service logs
docker compose logs app

# Force recreate containers
docker compose down
docker compose up -d
```

## 📊 Monitoring and Maintenance

### Check Backup Health
```bash
# List recent backups
ls -la backups/database_backup_*.db | tail -5

# Check backup sizes
du -h backups/database_backup_*.db

# Verify latest backup
file backups/database_backup_$(ls backups/ | grep database_backup | sort | tail -1)
```

### Disk Space Management
```bash
# Check available space
df -h .

# Check backup directory size
du -sh backups/

# Clean up old backups automatically
./scripts/linux/cleanup_backups.sh 10
```

### Log Rotation
```bash
# Rotate large log files
if [ $(stat -c%s backup_log.txt) -gt 10485760 ]; then
    mv backup_log.txt backup_log_$(date +%Y%m%d).txt
    touch backup_log.txt
fi
```

This Linux backup system provides enterprise-grade database backup capabilities with comprehensive logging, error handling, and automation features. All scripts are designed to be robust and production-ready.
