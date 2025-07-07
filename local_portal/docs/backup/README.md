# Backup Documentation

This directory contains comprehensive documentation for the database backup system used in the portal application.

## Files

### Core Documentation
- **`BACKUP_README.md`** - Complete guide for Windows PowerShell backup scripts
- **`LINUX_BACKUP_README.md`** - Complete guide for Linux shell backup scripts

### Implementation Details
- **`BACKUP_IMPLEMENTATION_SUMMARY.md`** - Technical implementation details and architecture
- **`CROSS_PLATFORM_BACKUP_SUMMARY.md`** - Cross-platform compatibility overview

## Quick Reference

### Windows Users
See `BACKUP_README.md` for instructions on using PowerShell scripts in `../../scripts/windows/`

### Linux Users  
See `LINUX_BACKUP_README.md` for instructions on using shell scripts in `../../scripts/linux/`

### Developers
See implementation summaries for technical details about the backup system architecture and cross-platform design.

## Related Files
- Backup scripts: `../../scripts/windows/` and `../../scripts/linux/`
- Docker configuration: `../../docker-compose.yml`
- Database location: `../../data/database.db`
- Backup storage: `../../backups/`
