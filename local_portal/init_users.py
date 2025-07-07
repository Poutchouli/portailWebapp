#!/usr/bin/env python3
"""
Initialization script to create initial admin and test users.
This should be run once to set up the initial user accounts.
"""

import os
import sys
from sqlmodel import Session, create_engine, select
from passlib.context import CryptContext

# Add the current directory to path to import our models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import User, create_db_and_tables

# Database setup
DATABASE_FILE = os.getenv("DATABASE_FILE", "database.db")
sqlite_url = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(sqlite_url, echo=True)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def create_initial_users():
    """Create initial admin and test users."""
    
    # Ensure tables exist
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if any users already exist
        existing_users = session.exec(select(User)).all()
        if existing_users:
            print(f"Found {len(existing_users)} existing users. Skipping user creation.")
            for user in existing_users:
                print(f"  - {user.username} (roles: {user.roles})")
            return
        
        # Create initial users
        users_to_create = [
            {
                "username": "admin",
                "password": "admin123",
                "roles": "admin,user"
            },
            {
                "username": "testuser", 
                "password": "user123",
                "roles": "user"
            },
            {
                "username": "manager",
                "password": "manager123", 
                "roles": "user,project_manager"
            },
            {
                "username": "specialuser",
                "password": "special123",
                "roles": "admin,user,special_access"
            }
        ]
        
        for user_data in users_to_create:
            hashed_password = get_password_hash(user_data["password"])
            db_user = User(
                username=user_data["username"],
                hashed_password=hashed_password, 
                roles=user_data["roles"]
            )
            session.add(db_user)
            print(f"Created user: {user_data['username']} (roles: {user_data['roles']})")
        
        session.commit()
        print(f"\nSuccessfully created {len(users_to_create)} initial users!")
        print("\nYou can now log in with:")
        for user_data in users_to_create:
            print(f"  Username: {user_data['username']}, Password: {user_data['password']}")

if __name__ == "__main__":
    create_initial_users()
