import sqlite3
import sys

# Connect to the database
db_path = '/app/data/database.db' if len(sys.argv) == 1 else sys.argv[1]
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== DATABASE CONTENTS VERIFICATION ===\n")

print("USERS:")
cursor.execute('SELECT id, username FROM user ORDER BY id')
users = cursor.fetchall()
for user in users:
    print(f"  ID: {user[0]}, Username: {user[1]}")

print("\nROLES:")
cursor.execute('SELECT id, name FROM role ORDER BY id')
roles = cursor.fetchall()
for role in roles:
    print(f"  ID: {role[0]}, Name: {role[1]}")

print("\nWEB APPLICATIONS:")
cursor.execute('SELECT id, name, url FROM webapp ORDER BY id')
webapps = cursor.fetchall()
for app in webapps:
    print(f"  ID: {app[0]}, Name: {app[1]}")
    print(f"      URL: {app[2]}")

print("\nUSER-ROLE ASSIGNMENTS:")
cursor.execute('''
    SELECT u.username, r.name 
    FROM user u
    JOIN userrolelink url ON u.id = url.user_id
    JOIN role r ON url.role_id = r.id
    ORDER BY u.username, r.name
''')
user_roles = cursor.fetchall()
for assignment in user_roles:
    print(f"  {assignment[0]} -> {assignment[1]}")

print("\nWEBAPP-ROLE REQUIREMENTS:")
cursor.execute('''
    SELECT w.name, r.name 
    FROM webapp w
    JOIN webapprolelink wrl ON w.id = wrl.webapp_id
    JOIN role r ON wrl.role_id = r.id
    ORDER BY w.name, r.name
''')
webapp_roles = cursor.fetchall()
for requirement in webapp_roles:
    print(f"  {requirement[0]} requires: {requirement[1]}")

conn.close()
print("\n=== VERIFICATION COMPLETE ===")
