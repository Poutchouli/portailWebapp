# Documentation

This directory contains all documentation for the portal application, organized by topic and purpose.

## Directory Structure

```
docs/
├── README.md                    # This file - documentation overview
├── USER_MANAGEMENT_TESTING.md  # User management API testing guide
├── backup/                      # Database backup system documentation
│   ├── README.md
│   ├── BACKUP_README.md         # Windows PowerShell backup guide
│   ├── LINUX_BACKUP_README.md  # Linux shell backup guide
│   ├── BACKUP_IMPLEMENTATION_SUMMARY.md
│   └── CROSS_PLATFORM_BACKUP_SUMMARY.md
└── setup/                       # Platform setup and installation guides
    ├── README.md
    ├── WINDOWS_SETUP.md         # Windows/Docker Desktop setup
    └── DOCKER_SETUP.md          # Linux/Docker setup
```

## Quick Navigation

### For End Users
- **Getting Started**: See `setup/` for platform-specific installation guides
- **Backup Management**: See `backup/` for database backup instructions
- **API Testing**: See `USER_MANAGEMENT_TESTING.md` for API testing procedures

### For Developers
- **Implementation Details**: See `backup/BACKUP_IMPLEMENTATION_SUMMARY.md`
- **Cross-Platform Design**: See `backup/CROSS_PLATFORM_BACKUP_SUMMARY.md`

### For System Administrators
- **Automated Backups**: See `backup/LINUX_BACKUP_README.md` for cron setup
- **Deployment**: See `setup/` for Docker deployment guides

## Related Directories
- **Scripts**: `../scripts/` contains all executable scripts
- **Configuration**: `../docker-compose.yml`, `../Dockerfile`
- **Application Code**: `../main.py`, `../portal-frontend-vue/`

## Contributing
When adding new documentation:
1. Place platform-specific docs in appropriate subdirectories
2. Update relevant README.md files
3. Keep file paths relative to project root
4. Follow existing naming conventions
