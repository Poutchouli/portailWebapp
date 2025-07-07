#!/bin/bash

# restore_db.sh
# Script to restore a backup file to the active database

# --- Configuration ---
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BACKUP_DIR="${PROJECT_ROOT}/backups"
DATA_DIR="${PROJECT_ROOT}/data"
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

list_backups() {
    echo "Available backup files:"
    local backups=($(ls -1t "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null))
    
    if [ ${#backups[@]} -eq 0 ]; then
        echo "No backup files found in ${BACKUP_DIR}"
        exit 1
    fi
    
    for i in "${!backups[@]}"; do
        local backup_file="${backups[$i]}"
        local size=$(du -h "$backup_file" | cut -f1)
        local date=$(stat -c %y "$backup_file" | cut -d' ' -f1,2 | cut -d'.' -f1)
        echo "  [$((i+1))] $(basename "$backup_file") ($size) - $date"
    done
    
    echo
}

select_backup() {
    local backups=($(ls -1t "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null))
    
    if [ -n "$1" ]; then
        # Backup file specified as argument
        if [ -f "${BACKUP_DIR}/$1" ]; then
            echo "$1"
            return 0
        elif [ -f "$1" ]; then
            echo "$(basename "$1")"
            return 0
        else
            echo "ERROR: Backup file '$1' not found" >&2
            exit 1
        fi
    fi
    
    # Interactive selection
    list_backups
    
    read -p "Enter the number of the backup to restore (or 'q' to quit): " choice
    
    if [ "$choice" = "q" ] || [ "$choice" = "Q" ]; then
        echo "Restore cancelled."
        exit 0
    fi
    
    if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
        echo "Invalid selection. Exiting."
        exit 1
    fi
    
    local index=$((choice - 1))
    if [ $index -lt 0 ] || [ $index -ge ${#backups[@]} ]; then
        echo "Invalid selection. Exiting."
        exit 1
    fi
    
    echo "$(basename "${backups[$index]}")"
}

# --- Main Script ---
echo "=== Portal Database Restore Script ==="

# Pre-flight checks
check_docker

if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found in ${PROJECT_ROOT}"
    exit 1
fi

# Ensure directories exist
mkdir -p "$BACKUP_DIR"
mkdir -p "$DATA_DIR"

# Select backup file
BACKUP_FILE=$(select_backup "$1")
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_FILE}"

if [ ! -f "$BACKUP_PATH" ]; then
    echo "ERROR: Backup file '$BACKUP_FILE' not found in ${BACKUP_DIR}"
    exit 1
fi

echo
echo "Selected backup: $BACKUP_FILE"
BACKUP_SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
BACKUP_DATE=$(stat -c %y "$BACKUP_PATH" | cut -d'.' -f1)
echo "Size: $BACKUP_SIZE | Created: $BACKUP_DATE"

# Confirm restore operation
echo
echo "WARNING: This will REPLACE your current database with the selected backup!"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo
echo "=== Starting Restore Process ==="
log_message "Starting database restore from ${BACKUP_FILE}"

# Step 1: Stop the app service
echo "Step 1: Stopping app service..."
log_message "Stopping app service for restore..."
docker compose stop app >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    log_message "WARNING: Failed to stop app service"
    echo "Warning: Could not stop app service. Continuing anyway..."
fi

# Step 2: Create safety backup if current database exists
if [ -f "${DATA_DIR}/database.db" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    SAFETY_BACKUP="${BACKUP_DIR}/pre_restore_backup_${TIMESTAMP}.db"
    echo "Step 2: Creating safety backup of current database..."
    log_message "Creating safety backup: ${SAFETY_BACKUP}"
    
    cp "${DATA_DIR}/database.db" "$SAFETY_BACKUP"
    if [ $? -eq 0 ]; then
        echo "Safety backup created: $(basename "$SAFETY_BACKUP")"
        log_message "Safety backup created successfully"
    else
        echo "WARNING: Failed to create safety backup"
        log_message "WARNING: Failed to create safety backup"
    fi
else
    echo "Step 2: No existing database found, skipping safety backup"
    log_message "No existing database found for safety backup"
fi

# Step 3: Restore the backup
echo "Step 3: Restoring backup file..."
log_message "Restoring backup from ${BACKUP_PATH} to ${DATA_DIR}/database.db"

cp "$BACKUP_PATH" "${DATA_DIR}/database.db"
if [ $? -eq 0 ]; then
    echo "Database file restored successfully"
    log_message "Database restore completed successfully"
else
    echo "ERROR: Failed to restore database file"
    log_message "ERROR: Failed to restore database file"
    exit 1
fi

# Step 4: Start the app service
echo "Step 4: Starting app service..."
log_message "Starting app service after restore..."

docker compose start app >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo
    echo "=== Restore Complete ==="
    echo "Database has been restored from: $BACKUP_FILE"
    echo "Your application should be running again on http://localhost:8000"
    log_message "Restore process completed successfully"
else
    echo
    echo "ERROR: Failed to start app service after restore."
    echo "You may need to run 'docker compose start app' manually."
    log_message "ERROR: Failed to start app service after restore"
    exit 1
fi
