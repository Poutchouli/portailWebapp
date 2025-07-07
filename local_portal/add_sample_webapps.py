#!/usr/bin/env python3
import sqlite3

# Connect to the database
conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

# Sample web applications to add
webapps = [
    {
        'name': 'User Management Portal',
        'url': 'http://localhost:8001',
        'description': 'Admin portal for managing users and permissions',
        'roles': ['admin']
    },
    {
        'name': 'Simple User Dashboard',
        'url': 'http://localhost:8002',
        'description': 'Basic user dashboard with personal information',
        'roles': ['user', 'admin']
    },
    {
        'name': 'Project Management Tool',
        'url': 'http://localhost:8003',
        'description': 'Tool for managing projects and tasks',
        'roles': ['project_manager', 'admin']
    },
    {
        'name': 'Special Access Portal',
        'url': 'http://localhost:8004',
        'description': 'Portal with restricted access for special users',
        'roles': ['special_access', 'admin']
    },
    {
        'name': 'Public Information Hub',
        'url': 'http://localhost:8005',
        'description': 'Public information accessible to all users',
        'roles': ['user', 'admin', 'project_manager', 'special_access']
    }
]

# Get role IDs
role_map = {}
cursor.execute("SELECT id, name FROM role")
roles = cursor.fetchall()
for role_id, role_name in roles:
    role_map[role_name] = role_id

print("Available roles:", role_map)

# Add web applications
for webapp in webapps:
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
    SELECT u.username, w.name 
    FROM user u
    JOIN userrolelink url ON u.id = url.user_id
    JOIN webapprolelink wrl ON url.role_id = wrl.role_id
    JOIN webapp w ON wrl.webapp_id = w.id
    ORDER BY u.username, w.name
""")
user_webapps = cursor.fetchall()

current_user = None
for username, webapp_name in user_webapps:
    if username != current_user:
        print(f"\nUser '{username}':")
        current_user = username
    print(f"  - {webapp_name}")

conn.close()
print("\nSample web applications added successfully!")
