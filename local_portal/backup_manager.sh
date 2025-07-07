#!/bin/bash

# backup_manager.sh
# Comprehensive backup management script with menu interface

# --- Configuration ---
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BACKUP_DIR="${PROJECT_ROOT}/backups"
LOG_FILE="${PROJECT_ROOT}/backup_log.txt"

# --- Functions ---
show_menu() {
    clear
    echo "======================================"
    echo "    DATABASE BACKUP MANAGEMENT        "
    echo "======================================"
    echo
    echo "1. Create Safe Backup (stops service)"
    echo "2. Create Quick Backup (service running)"
    echo "3. List Backup Files"
    echo "4. Restore Database"
    echo "5. Cleanup Old Backups"
    echo "6. View Backup Statistics"
    echo "7. View Recent Logs"
    echo "0. Exit"
    echo
}

check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        echo "ERROR: Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo "ERROR: Docker daemon is not running"
        exit 1
    fi
    
    if [ ! -f "${PROJECT_ROOT}/docker-compose.yml" ]; then
        echo "ERROR: docker-compose.yml not found in ${PROJECT_ROOT}"
        exit 1
    fi
    
    # Create backup directory if it doesn't exist
    mkdir -p "$BACKUP_DIR"
}

get_backup_stats() {
    echo "=== Backup Statistics ==="
    
    local backups=($(ls -1 "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null))
    
    if [ ${#backups[@]} -eq 0 ]; then
        echo "No backup files found."
        return
    fi
    
    local total_size=0
    local oldest_file=""
    local newest_file=""
    local oldest_time=9999999999
    local newest_time=0
    
    for backup in "${backups[@]}"; do
        local size=$(du -b "$backup" | cut -f1)
        local mtime=$(stat -c %Y "$backup")
        
        total_size=$((total_size + size))
        
        if [ $mtime -lt $oldest_time ]; then
            oldest_time=$mtime
            oldest_file="$backup"
        fi
        
        if [ $mtime -gt $newest_time ]; then
            newest_time=$mtime
            newest_file="$backup"
        fi
    done
    
    # Format sizes
    local total_kb=$((total_size / 1024))
    local total_mb=$((total_size / 1048576))
    local avg_size=$((total_size / ${#backups[@]} / 1024))
    
    echo "Total backup files: ${#backups[@]}"
    echo "Total space used: ${total_kb} KB (${total_mb} MB)"
    echo "Average backup size: ${avg_size} KB"
    
    if [ -n "$oldest_file" ]; then
        local oldest_date=$(stat -c %y "$oldest_file" | cut -d'.' -f1)
        echo "Oldest backup: $(basename "$oldest_file") ($oldest_date)"
    fi
    
    if [ -n "$newest_file" ]; then
        local newest_date=$(stat -c %y "$newest_file" | cut -d'.' -f1)
        echo "Newest backup: $(basename "$newest_file") ($newest_date)"
    fi
}

list_backups() {
    echo "=== Available Backup Files ==="
    
    local backups=($(ls -1t "${BACKUP_DIR}"/database_backup_*.db 2>/dev/null))
    
    if [ ${#backups[@]} -eq 0 ]; then
        echo "No backup files found."
        return
    fi
    
    for i in "${!backups[@]}"; do
        local backup="${backups[$i]}"
        local size=$(du -h "$backup" | cut -f1)
        local date=$(stat -c %y "$backup" | cut -d'.' -f1)
        local now=$(date +%s)
        local file_time=$(stat -c %Y "$backup")
        local age_seconds=$((now - file_time))
        
        local age_text=""
        if [ $age_seconds -gt 86400 ]; then
            local days=$((age_seconds / 86400))
            age_text="${days} days ago"
        elif [ $age_seconds -gt 3600 ]; then
            local hours=$((age_seconds / 3600))
            age_text="${hours} hours ago"
        else
            local minutes=$((age_seconds / 60))
            age_text="${minutes} minutes ago"
        fi
        
        echo "  [$((i+1))] $(basename "$backup")"
        echo "      Size: $size | Created: $age_text | Date: $date"
    done
}

view_recent_logs() {
    echo "=== Recent Backup Logs ==="
    
    if [ ! -f "$LOG_FILE" ]; then
        echo "No log file found."
        return
    fi
    
    echo "Showing last 20 log entries:"
    echo "----------------------------"
    tail -20 "$LOG_FILE"
}

run_safe_backup() {
    echo "Executing safe backup..."
    if [ -f "${PROJECT_ROOT}/backup_db.sh" ]; then
        "${PROJECT_ROOT}/backup_db.sh"
    else
        echo "ERROR: backup_db.sh script not found"
    fi
}

run_quick_backup() {
    echo "Executing quick backup..."
    if [ -f "${PROJECT_ROOT}/quick_backup.sh" ]; then
        "${PROJECT_ROOT}/quick_backup.sh"
    else
        echo "ERROR: quick_backup.sh script not found"
    fi
}

run_restore() {
    echo "Executing database restore..."
    if [ -f "${PROJECT_ROOT}/restore_db.sh" ]; then
        "${PROJECT_ROOT}/restore_db.sh"
    else
        echo "ERROR: restore_db.sh script not found"
    fi
}

run_cleanup() {
    echo "Executing backup cleanup..."
    if [ -f "${PROJECT_ROOT}/cleanup_backups.sh" ]; then
        "${PROJECT_ROOT}/cleanup_backups.sh"
    else
        echo "ERROR: cleanup_backups.sh script not found"
    fi
}

wait_for_key() {
    echo
    read -p "Press Enter to continue..."
}

# --- Main Script ---
check_prerequisites

# Main menu loop
while true; do
    show_menu
    read -p "Select an option (0-7): " choice
    
    case $choice in
        1)
            run_safe_backup
            wait_for_key
            ;;
        2)
            run_quick_backup
            wait_for_key
            ;;
        3)
            clear
            list_backups
            wait_for_key
            ;;
        4)
            run_restore
            wait_for_key
            ;;
        5)
            run_cleanup
            wait_for_key
            ;;
        6)
            clear
            get_backup_stats
            wait_for_key
            ;;
        7)
            clear
            view_recent_logs
            wait_for_key
            ;;
        0)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            sleep 2
            ;;
    esac
done
