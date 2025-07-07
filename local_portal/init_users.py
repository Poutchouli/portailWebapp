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

from main import User, Role, create_db_and_tables

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
                role_names = [role.name for role in user.roles]
                print(f"  - {user.username} (roles: {role_names})")
            return
        
        # Create initial users
        users_to_create = [
            {
                "username": "admin",
                "password": "admin123",
                "roles": ["admin", "user"]
            },
            {
                "username": "testuser", 
                "password": "user123",
                "roles": ["user"]
            },
            {
                "username": "manager",
                "password": "manager123", 
                "roles": ["user", "project_manager"]
            },
            {
                "username": "specialuser",
                "password": "special123",
                "roles": ["admin", "user", "special_access"]
            }
        ]
        
        for user_data in users_to_create:
            hashed_password = get_password_hash(user_data["password"])
            
            # Create the User object
            db_user = User(
                username=user_data["username"],
                hashed_password=hashed_password
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)  # Get the auto-generated ID
            
            # Add roles to the user
            for role_name in user_data["roles"]:
                role = session.exec(select(Role).where(Role.name == role_name)).first()
                if role:
                    db_user.roles.append(role)
                else:
                    print(f"Warning: Role '{role_name}' not found for user {user_data['username']}")
            
            session.commit()
            print(f"Created user: {user_data['username']} (roles: {user_data['roles']})")
        
        print(f"\nSuccessfully created {len(users_to_create)} initial users!")
        print("\nYou can now log in with:")
        for user_data in users_to_create:
            print(f"  Username: {user_data['username']}, Password: {user_data['password']}")

if __name__ == "__main__":
    create_initial_users()
