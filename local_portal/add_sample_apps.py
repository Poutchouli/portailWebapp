#!/usr/bin/env python3
"""
Script to add sample web applications to the database for testing.
"""

import sqlite3
import json
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "data" / "database.db"

def add_sample_apps():
    """Add sample web applications to the database."""
    
    print("Adding sample web applications to the database...")
    
    # Sample web applications
    sample_apps = [
        {
            "name": "Admin Dashboard",
            "description": "Administrative dashboard for system management",
            "url": "http://localhost:3001",
            "roles": ["admin"]
        },
        {
            "name": "Simple User App",
            "description": "Basic application for regular users",
            "url": "http://localhost:3002",
            "roles": ["user", "admin"]
        },
        {
            "name": "Analytics Portal",
            "description": "Data analytics and reporting portal",
            "url": "http://localhost:3003",
            "roles": ["analyst", "admin"]
        },
        {
            "name": "Public Documentation",
            "description": "Public documentation and help center",
            "url": "http://localhost:3004",
            "roles": ["user", "admin", "guest"]
        }
    ]
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Add sample applications
    for app in sample_apps:
        try:
            cursor.execute("""
                INSERT INTO web_apps (name, description, url, roles)
                VALUES (?, ?, ?, ?)
            """, (
                app["name"],
                app["description"],
                app["url"],
                json.dumps(app["roles"])
            ))
            print(f"✓ Added: {app['name']}")
        except sqlite3.IntegrityError:
            print(f"⚠ Already exists: {app['name']}")
    
    conn.commit()
    
    # Verify the apps were added
    cursor.execute("SELECT * FROM web_apps")
    apps = cursor.fetchall()
    
    print(f"\nTotal web applications in database: {len(apps)}")
    for app in apps:
        app_id, name, description, url, roles = app
        print(f"  {app_id}: {name} - {url} (roles: {roles})")
    
    conn.close()
    print("\nSample web applications added successfully!")

if __name__ == "__main__":
    add_sample_apps()
