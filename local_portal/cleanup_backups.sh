#!/bin/bash

# cleanup_backups.sh
# Script to clean up old backup files

# --- Configuration ---
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BACKUP_DIR="${PROJECT_ROOT}/backups"
LOG_FILE="${PROJECT_ROOT}/backup_log.txt"

# Default number of backups to keep
DEFAULT_KEEP=10

# --- Functions ---
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

show_usage() {
    echo "Usage: $0 [number_to_keep]"
    echo "  number_to_keep: Number of most recent backups to keep (default: $DEFAULT_KEEP)"
    echo "Example: $0 5    # Keep only the 5 most recent backups"
}

format_size() {
    local size_bytes=$1
    if [ $size_bytes -gt 1073741824 ]; then
        echo "$(awk "BEGIN {printf \"%.2f\", $size_bytes/1073741824}") GB"
    elif [ $size_bytes -gt 1048576 ]; then
        echo "$(awk "BEGIN {printf \"%.2f\", $size_bytes/1048576}") MB"
    elif [ $size_bytes -gt 1024 ]; then
        echo "$(awk "BEGIN {printf \"%.2f\", $size_bytes/1024}") KB"
    else
        echo "$size_bytes bytes"
    fi
}

# --- Main Script ---
KEEP_LAST=${1:-$DEFAULT_KEEP}

# Validate input
if ! [[ "$KEEP_LAST" =~ ^[0-9]+$ ]] || [ "$KEEP_LAST" -lt 1 ]; then
    echo "ERROR: Please provide a valid positive number of backups to keep"
    show_usage
    exit 1
fi

echo "=== Backup Cleanup Script ==="
echo "This script will keep the $KEEP_LAST most recent backups and delete the rest."
echo

# Check if backups directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backups directory not found: $BACKUP_DIR"
    exit 1
fi

# Get all backup files sorted by modification time (newest first)
mapfile -t all_backups < <(ls -1t "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null)

if [ ${#all_backups[@]} -eq 0 ]; then
    echo "No backup files found."
    exit 0
fi

echo "Found ${#all_backups[@]} backup files."

if [ ${#all_backups[@]} -le $KEEP_LAST ]; then
    echo "All backup files will be kept (found ${#all_backups[@]}, keeping $KEEP_LAST)."
    exit 0
fi

# Split into files to keep and files to delete
to_keep=("${all_backups[@]:0:$KEEP_LAST}")
to_delete=("${all_backups[@]:$KEEP_LAST}")

# Show files that will be kept
echo
echo "Backup files to KEEP (most recent $KEEP_LAST):"
for backup in "${to_keep[@]}"; do
    size=$(du -b "$backup" | cut -f1)
    formatted_size=$(format_size $size)
    date=$(stat -c %y "$backup" | cut -d'.' -f1)
    echo "  ✓ $(basename "$backup") ($formatted_size) - $date"
done

# Show files that will be deleted
echo
echo "Backup files to DELETE:"
total_delete_size=0
for backup in "${to_delete[@]}"; do
    size=$(du -b "$backup" | cut -f1)
    total_delete_size=$((total_delete_size + size))
    formatted_size=$(format_size $size)
    date=$(stat -c %y "$backup" | cut -d'.' -f1)
    echo "  ✗ $(basename "$backup") ($formatted_size) - $date"
done

formatted_total_size=$(format_size $total_delete_size)
echo
echo "This will free up $formatted_total_size of disk space."

# Confirm deletion
echo
read -p "Proceed with deletion? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Delete old backups
echo
echo "Deleting old backup files..."
log_message "Starting cleanup - keeping $KEEP_LAST backups, deleting ${#to_delete[@]} files"

deleted_count=0
deleted_size=0

for backup in "${to_delete[@]}"; do
    size=$(du -b "$backup" | cut -f1)
    if rm "$backup" 2>/dev/null; then
        echo "  Deleted: $(basename "$backup")"
        log_message "Deleted backup: $(basename "$backup") ($size bytes)"
        deleted_count=$((deleted_count + 1))
        deleted_size=$((deleted_size + size))
    else
        echo "  Failed to delete: $(basename "$backup")"
        log_message "ERROR: Failed to delete backup: $(basename "$backup")"
    fi
done

echo
echo "=== Cleanup Complete ==="
formatted_deleted_size=$(format_size $deleted_size)
echo "Deleted $deleted_count backup files ($formatted_deleted_size)."
echo "Kept ${#to_keep[@]} most recent backup files."
log_message "Cleanup completed - deleted $deleted_count files, freed $formatted_deleted_size"

# Show remaining files
echo
echo "Remaining backup files:"
mapfile -t remaining < <(ls -1t "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null)
for backup in "${remaining[@]}"; do
    size=$(du -b "$backup" | cut -f1)
    formatted_size=$(format_size $size)
    date=$(stat -c %y "$backup" | cut -d'.' -f1)
    echo "  $(basename "$backup") ($formatted_size) - $date"
done
