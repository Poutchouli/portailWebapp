#!/bin/bash

# backup_db.sh
# Script to back up the SQLite database from the Docker Compose volume

# --- Configuration ---
# Path to your local_portal project directory (where docker-compose.yml is)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Directory paths
BACKUP_DIR="${PROJECT_ROOT}/backups"
LOG_FILE="${PROJECT_ROOT}/backup_log.txt"

# --- Functions ---
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

print_separator() {
    echo "========================================" | tee -a "$LOG_FILE"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_message "ERROR: Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_message "ERROR: Docker daemon is not running"
        exit 1
    fi
}

check_compose_file() {
    if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
        log_message "ERROR: docker-compose.yml not found in ${PROJECT_ROOT}"
        exit 1
    fi
}

# --- Main Script ---
print_separator
log_message "Starting database backup process..."
log_message "Project root: ${PROJECT_ROOT}"

# Pre-flight checks
check_docker
check_compose_file

# Ensure the backup directory exists
mkdir -p "$BACKUP_DIR"
log_message "Backup directory: ${BACKUP_DIR}"

# Check if app service is running
APP_STATUS=$(docker compose ps app --format json 2>/dev/null | jq -r '.State' 2>/dev/null || echo "unknown")
log_message "Current app service status: ${APP_STATUS}"

# 1. Stop the app service for a consistent SQLite backup
log_message "Stopping app service for consistent backup..."
docker compose stop app >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    log_message "WARNING: Failed to stop app service. Continuing with backup anyway..."
    # Don't exit here, as the service might already be stopped
else
    log_message "App service stopped successfully."
fi

# 2. Run the backup container
log_message "Running backup-db container..."
# Capture the backup output
BACKUP_OUTPUT=$(docker compose run --rm backup-db 2>&1)
BACKUP_EXIT_CODE=$?

# Log the backup output
echo "$BACKUP_OUTPUT" >> "$LOG_FILE"
echo "$BACKUP_OUTPUT"

if [ $BACKUP_EXIT_CODE -ne 0 ]; then
    log_message "ERROR: Failed to run backup-db container. Backup might not have completed."
    # Attempt to restart app even if backup failed
    if [ "$APP_STATUS" = "running" ]; then
        log_message "Attempting to restart app service..."
        docker compose start app >> "$LOG_FILE" 2>&1
    fi
    exit 1
fi

# Extract timestamp from backup output for verification
BACKUP_FILE=$(echo "$BACKUP_OUTPUT" | grep -o "database_backup_[0-9_]*\.db" | head -1)
if [ -n "$BACKUP_FILE" ]; then
    log_message "Backup file created: ${BACKUP_FILE}"
    
    # Verify backup file exists locally
    if [ -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
        BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
        log_message "Backup verified locally - Size: ${BACKUP_SIZE}"
    else
        log_message "WARNING: Backup file not found locally at ${BACKUP_DIR}/${BACKUP_FILE}"
    fi
else
    log_message "WARNING: Could not determine backup filename from output"
fi

# 3. Restart the app service if it was running before
if [ "$APP_STATUS" = "running" ]; then
    log_message "Starting app service..."
    docker compose start app >> "$LOG_FILE" 2>&1
    if [ $? -ne 0 ]; then
        log_message "ERROR: Failed to start app service. Manual intervention required."
        log_message "Try running: docker compose start app"
        exit 1
    fi
    log_message "App service started successfully."
else
    log_message "App service was not running before backup, leaving it stopped."
fi

# 4. Summary
print_separator
log_message "Database backup process completed successfully!"

# List recent backups
RECENT_BACKUPS=$(ls -la "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null | tail -5)
if [ -n "$RECENT_BACKUPS" ]; then
    log_message "Recent backup files:"
    echo "$RECENT_BACKUPS" | while read -r line; do
        log_message "  $line"
    done
else
    log_message "No backup files found in ${BACKUP_DIR}"
fi

# Disk usage summary
TOTAL_BACKUP_SIZE=$(du -sh "${BACKUP_DIR}" 2>/dev/null | cut -f1)
BACKUP_COUNT=$(ls -1 "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null | wc -l)
log_message "Total backups: ${BACKUP_COUNT}, Total size: ${TOTAL_BACKUP_SIZE}"

print_separator
