#!/usr/bin/env python3
import sqlite3

# Connect to the database
conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

print("Clearing existing web applications...")

# Delete existing webapp-role links
cursor.execute("DELETE FROM webapprolelink")
print("Cleared webapp-role links")

# Delete existing webapps
cursor.execute("DELETE FROM webapp")
print("Cleared webapps")

# Get role IDs
role_map = {}
cursor.execute("SELECT id, name FROM role")
roles = cursor.fetchall()
for role_id, role_name in roles:
    role_map[role_name] = role_id

print("Available roles:", role_map)

# Add real web applications
real_webapps = [
    {
        'name': 'File Manager',
        'url': 'http://localhost:5001',
        'description': 'Simple user application for file management and user-level operations',
        'roles': ['user']
    },
    {
        'name': 'Admin Dashboard',
        'url': 'http://localhost:5002',
        'description': 'Administrative dashboard for system management and user administration',
        'roles': ['admin']
    }
]

# Add the real web applications
for webapp in real_webapps:
    # Insert webapp
    cursor.execute(
        "INSERT INTO webapp (name, url, description) VALUES (?, ?, ?)",
        (webapp['name'], webapp['url'], webapp['description'])
    )
    webapp_id = cursor.lastrowid
    print(f"Added webapp: {webapp['name']} (ID: {webapp_id})")
    
    # Link webapp to roles
    for role_name in webapp['roles']:
        if role_name in role_map:
            role_id = role_map[role_name]
            cursor.execute(
                "INSERT INTO webapprolelink (webapp_id, role_id) VALUES (?, ?)",
                (webapp_id, role_id)
            )
            print(f"  Linked to role: {role_name} (ID: {role_id})")
        else:
            print(f"  Warning: Role '{role_name}' not found")

# Commit changes
conn.commit()

# Verify the data
print("\n--- Verification ---")
cursor.execute("SELECT COUNT(*) FROM webapp")
webapp_count = cursor.fetchone()[0]
print(f"Total webapps: {webapp_count}")

cursor.execute("SELECT COUNT(*) FROM webapprolelink")
link_count = cursor.fetchone()[0]
print(f"Total webapp-role links: {link_count}")

# Show webapps for each user
print("\n--- Webapps accessible by each user ---")
cursor.execute("""
    SELECT u.username, w.name, w.url
    FROM user u
    JOIN userrolelink url ON u.id = url.user_id
    JOIN webapprolelink wrl ON url.role_id = wrl.role_id
    JOIN webapp w ON wrl.webapp_id = w.id
    ORDER BY u.username, w.name
""")
user_webapps = cursor.fetchall()

current_user = None
for username, webapp_name, webapp_url in user_webapps:
    if username != current_user:
        print(f"\nUser '{username}':")
        current_user = username
    print(f"  - {webapp_name} ({webapp_url})")

conn.close()
print("\nReal web applications configured successfully!")
