#!/bin/bash

# setup_cron.sh
# Helper script to set up automated backups using cron

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BACKUP_SCRIPT="${PROJECT_ROOT}/backup_db.sh"

show_usage() {
    echo "Usage: $0 [schedule_type]"
    echo
    echo "Schedule types:"
    echo "  daily     - Daily backup at 3:00 AM"
    echo "  weekly    - Weekly backup on Sunday at 2:30 AM"
    echo "  hourly6   - Every 6 hours (00:00, 06:00, 12:00, 18:00)"
    echo "  custom    - Enter custom cron schedule"
    echo "  list      - List current cron jobs"
    echo "  remove    - Remove backup cron job"
    echo
    echo "Example: $0 daily"
}

check_backup_script() {
    if [ ! -f "$BACKUP_SCRIPT" ]; then
        echo "ERROR: Backup script not found at $BACKUP_SCRIPT"
        exit 1
    fi
    
    if [ ! -x "$BACKUP_SCRIPT" ]; then
        echo "Making backup script executable..."
        chmod +x "$BACKUP_SCRIPT"
    fi
}

get_cron_line() {
    local schedule_type="$1"
    local cron_line=""
    
    case "$schedule_type" in
        "daily")
            cron_line="0 3 * * * $BACKUP_SCRIPT"
            echo "Daily backup at 3:00 AM"
            ;;
        "weekly")
            cron_line="30 2 * * SUN $BACKUP_SCRIPT"
            echo "Weekly backup on Sunday at 2:30 AM"
            ;;
        "hourly6")
            cron_line="0 */6 * * * $BACKUP_SCRIPT"
            echo "Backup every 6 hours"
            ;;
        "custom")
            echo "Enter custom cron schedule (format: minute hour day month weekday)"
            echo "Examples:"
            echo "  0 3 * * *     - Daily at 3:00 AM"
            echo "  30 2 * * SUN  - Weekly on Sunday at 2:30 AM"
            echo "  0 */6 * * *   - Every 6 hours"
            echo
            read -p "Enter cron schedule: " custom_schedule
            cron_line="$custom_schedule $BACKUP_SCRIPT"
            echo "Custom schedule: $custom_schedule"
            ;;
        *)
            echo "ERROR: Invalid schedule type"
            show_usage
            exit 1
            ;;
    esac
    
    echo "$cron_line"
}

list_cron_jobs() {
    echo "Current cron jobs:"
    echo "=================="
    crontab -l 2>/dev/null | grep -E "(backup|$BACKUP_SCRIPT)" || echo "No backup-related cron jobs found."
}

add_cron_job() {
    local cron_line="$1"
    local temp_cron=$(mktemp)
    
    # Get existing crontab (excluding our backup job)
    crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT" > "$temp_cron"
    
    # Add our backup job
    echo "$cron_line" >> "$temp_cron"
    
    # Install new crontab
    crontab "$temp_cron"
    rm "$temp_cron"
    
    if [ $? -eq 0 ]; then
        echo "Cron job added successfully!"
        echo "Backup will run according to schedule: $cron_line"
    else
        echo "ERROR: Failed to add cron job"
        exit 1
    fi
}

remove_cron_job() {
    local temp_cron=$(mktemp)
    
    # Get existing crontab (excluding our backup job)
    local existing_jobs=$(crontab -l 2>/dev/null | grep -v "$BACKUP_SCRIPT")
    
    if [ -z "$existing_jobs" ]; then
        echo "No backup cron jobs found to remove."
        return
    fi
    
    echo "$existing_jobs" > "$temp_cron"
    crontab "$temp_cron"
    rm "$temp_cron"
    
    if [ $? -eq 0 ]; then
        echo "Backup cron job removed successfully!"
    else
        echo "ERROR: Failed to remove cron job"
        exit 1
    fi
}

# Main script
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

case "$1" in
    "list")
        list_cron_jobs
        ;;
    "remove")
        echo "Removing backup cron job..."
        remove_cron_job
        ;;
    "daily"|"weekly"|"hourly6"|"custom")
        check_backup_script
        
        echo "=== Cron Backup Setup ==="
        echo "Project: $PROJECT_ROOT"
        echo "Backup script: $BACKUP_SCRIPT"
        echo
        
        cron_line=$(get_cron_line "$1")
        
        echo
        echo "This will add the following cron job:"
        echo "$cron_line"
        echo
        read -p "Continue? (yes/no): " confirm
        
        if [ "$confirm" = "yes" ]; then
            add_cron_job "$cron_line"
            echo
            echo "Current cron jobs:"
            crontab -l 2>/dev/null
        else
            echo "Setup cancelled."
        fi
        ;;
    *)
        echo "ERROR: Unknown option '$1'"
        show_usage
        exit 1
        ;;
esac
