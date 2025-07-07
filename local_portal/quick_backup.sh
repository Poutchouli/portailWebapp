#!/bin/bash

# quick_backup.sh
# Quick backup script that doesn't stop the service
# Use this for development or when you need a backup without downtime

# --- Configuration ---
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BACKUP_DIR="${PROJECT_ROOT}/backups"
LOG_FILE="${PROJECT_ROOT}/backup_log.txt"

# --- Functions ---
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "ERROR: Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo "ERROR: Docker daemon is not running"
        exit 1
    fi
}

# --- Main Script ---
echo "=== Quick Database Backup ==="
log_message "Starting quick backup (service will continue running)..."

# Pre-flight checks
check_docker

if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found in ${PROJECT_ROOT}"
    exit 1
fi

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Run the backup
echo "Creating backup..."
BACKUP_OUTPUT=$(docker compose run --rm backup-db 2>&1)
BACKUP_EXIT_CODE=$?

# Show output
echo "$BACKUP_OUTPUT"

# Log the output
echo "$BACKUP_OUTPUT" >> "$LOG_FILE"
log_message "Quick backup process completed with exit code: ${BACKUP_EXIT_CODE}"

if [ $BACKUP_EXIT_CODE -eq 0 ]; then
    echo "Quick backup completed successfully!"
    
    # Extract and verify backup filename
    BACKUP_FILE=$(echo "$BACKUP_OUTPUT" | grep -o "database_backup_[0-9_]*\.db" | head -1)
    if [ -n "$BACKUP_FILE" ] && [ -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
        BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
        echo "Backup file: ${BACKUP_FILE} (${BACKUP_SIZE})"
    fi
else
    echo "Backup failed!"
    exit 1
fi
