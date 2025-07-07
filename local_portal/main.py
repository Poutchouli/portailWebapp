# main.py
import os
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select

# Database setup
DATABASE_FILE = os.getenv("DATABASE_FILE", "database.db")
sqlite_url = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(sqlite_url, echo=True) # echo=True for logging SQL queries (useful for debugging)

def create_db_and_tables():
    """
    Creates all tables defined by SQLModel metadata if they don't already exist.
    """
    SQLModel.metadata.create_all(engine)

# User Model Definition
class User(SQLModel, table=True):
    """
    Represents a user in the system.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    hashed_password: str
    # For now, we'll keep roles simple as a string, but we can make it more sophisticated later.
    roles: str = Field(default="user", max_length=255) # Comma-separated roles, e.g., "admin,webapp1_access"

# Pydantic Schemas for API Requests/Responses
# These define what data we expect when creating/updating users,
# and what data we return. They can differ from the database model.

class UserCreate(SQLModel):
    """
    Schema for creating a new user.
    Password is required.
    """
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6) # Password field for input, will be hashed
    roles: str = "user" # Default role, can be overridden

class UserUpdate(SQLModel):
    """
    Schema for updating an existing user.
    All fields are optional, meaning you can update only specific ones.
    """
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    password: Optional[str] = Field(default=None, min_length=6)
    roles: Optional[str] = Field(default=None, max_length=255)

class UserResponse(SQLModel):
    """
    Schema for returning user data.
    Does NOT include the hashed password for security.
    """
    id: int
    username: str
    roles: str

# FastAPI Application
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from contextlib import asynccontextmanager

# Lifespan event handler for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for FastAPI application lifespan.
    Handles startup and shutdown events.
    """
    # Startup
    create_db_and_tables()
    print(f"Database tables created in {DATABASE_FILE}")
    yield
    # Shutdown (if needed)

app = FastAPI(title="Local Portal Backend", lifespan=lifespan)

# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper functions for password hashing/verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Local Portal Backend!"}

# --- User Management Endpoints ---

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Creates a new user.
    Expects username, password, and optional roles.
    Hashes the password before storing.
    """
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, roles=user.roles)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[UserResponse])
def read_users(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Retrieves a list of all users with pagination.
    (Admin access will be implemented later)
    """
    # Ensure limit doesn't exceed 100
    limit = min(limit, 100)
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, session: Session = Depends(get_session)):
    """
    Retrieves a single user by their ID.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    """
    Updates an existing user's details (username, password, roles).
    Only updates provided fields. Hashes new password if provided.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update fields if provided in the request
    if user_update.username is not None:
        # Check if new username already exists for another user
        existing_user = session.exec(select(User).where(User.username == user_update.username)).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered by another user"
            )
        user.username = user_update.username
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)
    if user_update.roles is not None:
        user.roles = user_update.roles

    session.add(user) # Re-add to session to mark as modified
    session.commit()
    session.refresh(user) # Refresh to get latest data from DB
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    Deletes a user by their ID.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    session.delete(user)
    session.commit()
    return {} # No content response for successful deletion

# You can run this file to create the database and tables initially
# or it will be done automatically on app startup.
if __name__ == "__main__":
    print("This script is primarily meant to be run by Uvicorn.")
    print("To run the application, use: uvicorn main:app --reload")
    print("Creating database and tables for initial setup if not present...")
    create_db_and_tables()
