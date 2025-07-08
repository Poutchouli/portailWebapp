# add_sample_webapps.py
# This script adds sample users and web applications to the database using SQLModel.

import os
from typing import List, Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlalchemy.orm import selectinload

# --- Re-import necessary models and functions from main.py ---
# To avoid circular imports or copying the whole main.py, we redefine
# the essential models and the get_or_create_roles function here.
# In a larger project, these models would be in a separate 'models.py'
# file, and utilities in 'utils.py' etc.

# Database setup
# This must match the database file used by the main FastAPI app inside the container
DATABASE_FILE = "database.db"
sqlite_url = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(sqlite_url, echo=False) # echo=True can be very verbose for seeding

# --- Models (Simplified for this script, mirroring main.py) ---
# For this seeding script, we'll use simplified models without relationships
# to avoid SQLAlchemy type errors. The main.py has the full relationship definitions.

# Association Table for User and Role (Many-to-Many)
class UserRoleLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)

# Association Table for WebApp and Role (Many-to-Many)
class WebAppRoleLink(SQLModel, table=True):
    webapp_id: Optional[int] = Field(default=None, foreign_key="webapp.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    hashed_password: str

class WebApp(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, min_length=3, max_length=100)
    url: str = Field(min_length=5)
    description: Optional[str] = Field(default=None, max_length=500)

# --- Password Hashing (from main.py) ---
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- Helper Function (from main.py) ---
async def get_or_create_roles(session: Session, role_names: List[str]) -> List[Role]:
    roles = []
    for role_name in role_names:
        role = session.exec(select(Role).where(Role.name == role_name)).first()
        if not role:
            print(f"Role '{role_name}' not found, creating it.")
            role = Role(name=role_name)
            session.add(role)
            session.commit()
            session.refresh(role)
        roles.append(role)
    return roles

# --- Data Seeding Logic ---
async def create_sample_data():
    """
    Creates sample users and web applications in the database.
    This script will re-add existing users/apps if run multiple times,
    but unique constraints (username, webapp name) will prevent duplicates.
    """
    # Create tables first
    SQLModel.metadata.create_all(engine)
    print("Database tables created.")
    
    with Session(engine) as session:
        print("Ensuring default roles exist...")
        default_roles_names = ["admin", "user", "project_manager", "special_access", "public"]
        for role_name in default_roles_names:
            role = session.exec(select(Role).where(Role.name == role_name)).first()
            if not role:
                session.add(Role(name=role_name))
                session.commit()
        print("Default roles ensured.")

        # --- Sample Users ---
        users_to_create = [
            {"username": "admin", "password": "admin123", "roles": ["admin", "user", "project_manager", "special_access", "public"]},
            {"username": "testuser", "password": "testpass", "roles": ["user", "public"]},
            {"username": "manager", "password": "managerpass", "roles": ["user", "project_manager", "public"]},
            {"username": "specialuser", "password": "specialpass", "roles": ["user", "special_access", "public"]}
        ]
        
        print("\nAdding/updating sample users...")
        for user_data in users_to_create:
            username = user_data["username"]
            password_hash = get_password_hash(user_data["password"])
            roles_names = user_data["roles"]

            existing_user = session.exec(select(User).where(User.username == username)).first()
            
            if not existing_user:
                print(f"Creating user: {username}")
                new_user = User(username=username, hashed_password=password_hash)
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                
                # Assign roles to the new user via UserRoleLink
                roles_to_assign = await get_or_create_roles(session, roles_names)
                for role in roles_to_assign:
                    user_role_link = UserRoleLink(user_id=new_user.id, role_id=role.id)
                    session.add(user_role_link)
                session.commit()
            else:
                print(f"User '{username}' already exists. Updating password and roles.")
                # Update password (if changed) and roles
                existing_user.hashed_password = password_hash # Always update password to ensure consistency
                
                # Update roles: clear existing and add new via UserRoleLink
                # First delete existing role links
                existing_links = session.exec(select(UserRoleLink).where(UserRoleLink.user_id == existing_user.id)).all()
                for link in existing_links:
                    session.delete(link)
                
                # Add new role links
                roles_to_assign = await get_or_create_roles(session, roles_names)
                for role in roles_to_assign:
                    user_role_link = UserRoleLink(user_id=existing_user.id, role_id=role.id)
                    session.add(user_role_link)
                
                session.add(existing_user)
                session.commit()

        # --- Sample WebApps ---
        webapps_to_create = [
            {"name": "User Management Portal", "url": "http://localhost:8000/admin/users", "roles": ["admin"], "description": "Admin UI for managing user accounts."},
            {"name": "Simple User Dashboard", "url": "http://localhost:5001", "roles": ["user", "admin", "public"], "description": "A basic application for all users."},
            {"name": "Admin Dashboard", "url": "http://localhost:5002", "roles": ["admin"], "description": "The administrative control panel."},
            {"name": "Project Management Tool", "url": "http://localhost:8082", "roles": ["project_manager", "admin", "public"], "description": "Tool to manage projects and tasks."},
            {"name": "Special Access Portal", "url": "http://localhost:8083", "roles": ["special_access", "admin"], "description": "Portal with advanced features for specific users."},
            {"name": "Public Information Hub", "url": "http://localhost:8084", "roles": ["public", "user", "admin"], "description": "Publicly accessible information for all visitors."}
        ]

        print("\nAdding/updating sample web applications...")
        for app_data in webapps_to_create:
            app_name = app_data["name"]
            app_roles_names = app_data["roles"]

            existing_app = session.exec(select(WebApp).where(WebApp.name == app_name)).first()

            if not existing_app:
                print(f"Creating webapp: {app_name}")
                new_app = WebApp(name=app_name, url=app_data["url"], description=app_data.get("description"))
                session.add(new_app)
                session.commit()
                session.refresh(new_app)

                # Assign roles to the new webapp via WebAppRoleLink
                roles_to_assign = await get_or_create_roles(session, app_roles_names)
                for role in roles_to_assign:
                    webapp_role_link = WebAppRoleLink(webapp_id=new_app.id, role_id=role.id)
                    session.add(webapp_role_link)
                session.commit()
            else:
                print(f"Webapp '{app_name}' already exists. Updating URL, description and roles.")
                existing_app.url = app_data["url"]
                existing_app.description = app_data.get("description")
                
                # Update roles: clear existing and add new via WebAppRoleLink
                # First delete existing role links
                existing_links = session.exec(select(WebAppRoleLink).where(WebAppRoleLink.webapp_id == existing_app.id)).all()
                for link in existing_links:
                    session.delete(link)
                
                # Add new role links
                roles_to_assign = await get_or_create_roles(session, app_roles_names)
                for role in roles_to_assign:
                    webapp_role_link = WebAppRoleLink(webapp_id=existing_app.id, role_id=role.id)
                    session.add(webapp_role_link)
                
                session.add(existing_app)
                session.commit()

    print("\nSample data seeding complete.")

# To run the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(create_sample_data())