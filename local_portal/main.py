# main.py
import os
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pydantic import field_validator
from fastapi import Request # IMPORT ADDED
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from contextlib import asynccontextmanager

# Database setup
DATABASE_FILE = os.getenv("DATABASE_FILE", "database.db")
sqlite_url = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(sqlite_url, echo=True) # echo=True for logging SQL queries (useful for debugging)

def create_db_and_tables():
    """
    Creates all tables defined by SQLModel metadata if they don't already exist.
    Also initializes default roles.
    """
    SQLModel.metadata.create_all(engine)
    print("Database tables created.")

    # NEW: Initialize default roles if they don't exist
    with Session(engine) as session:
        default_roles = ["admin", "user", "project_manager", "special_access"]
        for role_name in default_roles:
            role = session.exec(select(Role).where(Role.name == role_name)).first()
            if not role:
                new_role = Role(name=role_name)
                session.add(new_role)
                print(f"Added default role: {role_name}")
        session.commit()
        print("Default roles ensured.")

# NEW: Association Table for User and Role (Many-to-Many)
class UserRoleLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)

# NEW: Association Table for WebApp and Role (Many-to-Many)
class WebAppRoleLink(SQLModel, table=True):
    webapp_id: Optional[int] = Field(default=None, foreign_key="webapp.id", primary_key=True)
    role_id: Optional[int] = Field(default=None, foreign_key="role.id", primary_key=True)

# NEW: Role Model
class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)

    # Relationships (back-references)
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
    web_apps: List["WebApp"] = Relationship(back_populates="required_by_roles", link_model=WebAppRoleLink)

# UPDATED: User Model Definition
class User(SQLModel, table=True):
    """
    Represents a user in the system.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    hashed_password: str

    # NEW: Relationship to roles via UserRoleLink
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)

# UPDATED: Pydantic Schemas for API Requests/Responses

# UPDATED: Pydantic Model for User Creation
class UserCreate(SQLModel):
    """
    Schema for creating a new user.
    Password is required.
    """
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    roles: Optional[List[str]] = Field(default_factory=list) # Now a list of role names

# UPDATED: Pydantic Model for User Update (for partial updates)
class UserUpdate(SQLModel):
    """
    Schema for updating an existing user.
    All fields are optional, meaning you can update only specific ones.
    """
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    password: Optional[str] = Field(default=None, min_length=8)
    roles: Optional[List[str]] = Field(default=None) # Now a list of role names

# UPDATED: Pydantic Model for User Response (what we send back to the client, without the hashed password)
class UserResponse(SQLModel):
    """
    Schema for returning user data.
    Does NOT include the hashed password for security.
    """
    id: int
    username: str
    roles: List[str] # Now a list of role names

    # This method is for Pydantic to know how to create the response from the DB object
    model_config = {"from_attributes": True} # Use from_attributes for Pydantic v2

    @field_validator("roles", mode="before")
    @classmethod
    def extract_role_names(cls, roles_list):
        """Extracts role names from a list of Role objects."""
        if isinstance(roles_list, list) and all(hasattr(role, 'name') for role in roles_list):
            return [role.name for role in roles_list]
        return roles_list

# UPDATED: WebApp Model Definition
class WebApp(SQLModel, table=True):
    """
    Represents a web application that can be accessed via the portal.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, min_length=3, max_length=100)
    url: str = Field(min_length=5)
    description: Optional[str] = Field(default=None, max_length=500)

    # NEW: Relationship to roles via WebAppRoleLink
    required_by_roles: List["Role"] = Relationship(back_populates="web_apps", link_model=WebAppRoleLink)

# UPDATED: Pydantic Model for Web App Creation
class WebAppCreate(SQLModel):
    name: str = Field(min_length=3, max_length=100)
    url: str = Field(min_length=5)
    required_roles: Optional[List[str]] = Field(default_factory=list) # Now a list of role names
    description: Optional[str] = Field(default=None, max_length=500)

# UPDATED: Pydantic Model for Web App Response
class WebAppResponse(SQLModel):
    id: int
    name: str
    url: str
    required_roles: List[str] # Now a list of role names
    description: Optional[str] = None

    model_config = {"from_attributes": True} # Use from_attributes for Pydantic v2

    @field_validator("required_roles", mode="before")
    @classmethod
    def extract_role_names_webapp(cls, roles_list):
        """Extracts role names from a list of Role objects."""
        if isinstance(roles_list, list) and all(hasattr(role, 'name') for role in roles_list):
            return [role.name for role in roles_list]
        return roles_list

# UPDATED: Pydantic Model for Web App Update
class WebAppUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    url: Optional[str] = Field(default=None, min_length=5)
    required_roles: Optional[List[str]] = Field(default=None) # Now a list of role names
    description: Optional[str] = Field(default=None, max_length=500)

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production-use-secrets-token-urlsafe-32"  # IMPORTANT: CHANGE THIS IN PRODUCTION!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # How long the token is valid for

# Pydantic Model for JWT Token response
class Token(SQLModel):
    access_token: str
    token_type: str

# Pydantic Model for data stored in the JWT token (payload)
class TokenData(SQLModel):
    username: Optional[str] = None
    scopes: Optional[str] = None  # Will be used for roles/permissions later

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

# FastAPI Application
app = FastAPI(title="Local Portal Backend", lifespan=lifespan)

# CORS Middleware (allowing frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Password Bearer for token-based authentication
# This tells FastAPI where to look for the token (in the Authorization header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Utility Functions ---

# Helper functions for password hashing/verification
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)

def decode_access_token(token: str) -> Optional[TokenData]:
    """
    Decodes and validates a JWT access token.
    Returns TokenData if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        roles: Optional[str] = payload.get("roles")  # Get roles from token
        if username is None:
            return None  # No subject in token
        token_data = TokenData(username=username, scopes=roles)
    except JWTError:
        return None  # Invalid token
    return token_data

def get_or_create_roles(session: Session, role_names: List[str]) -> List[Role]:
    """
    Retrieves Role objects for given names, creating them if they don't exist.
    """
    roles = []
    for role_name in role_names:
        role = session.exec(select(Role).where(Role.name == role_name)).first()
        if not role:
            # This should ideally not happen for predefined roles,
            # but allows dynamic role creation if desired.
            role = Role(name=role_name)
            session.add(role)
            session.commit()
            session.refresh(role)
            print(f"Created new role: {role_name}")
        roles.append(role)
    return roles

# --- Authentication & User Dependencies ---

async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get the current authenticated user from the JWT token,
    eagerly loading their roles from the database.
    Raises HTTPException if authentication fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception

    # Optionally, verify the user still exists in the database
    if token_data.username is None:
        raise credentials_exception
    
    # Now eager load roles when fetching user
    user = session.exec(select(User).where(User.username == token_data.username)).first()
    if user is None:
        raise credentials_exception

    return user

# NEW: Dependency to get the current user and check if they are an admin
def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that checks if the current user has the 'admin' role.
    Raises an HTTPException if the user is not an admin.
    """
    user_role_names = [role.name for role in current_user.roles]
    if "admin" not in user_role_names:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted: Requires admin privileges",
        )
    return current_user

# API Endpoints
@app.get("/", include_in_schema=False)
async def serve_vue_app_root():
    """
    Serves the Vue.js SPA index.html as the root endpoint.
    """
    return FileResponse("portal-frontend-vue/dist/index.html")

# --- Web App Listing Endpoint ---

@app.get("/apps/", response_model=List[WebAppResponse]) # Changed response_model to WebAppResponse
async def get_available_apps(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)): # Added session dependency
    """
    Returns a list of web applications available to the current user based on their roles.
    Now fetches apps from the database with linked roles.
    """
    # Get the names of roles the current user has
    user_role_names = {role.name for role in current_user.roles} # Get set of names

    # Fetch all web apps from the database
    all_apps_from_db = session.exec(select(WebApp)).all()

    # Filter apps based on user roles and convert to response objects
    available_apps = []
    for app in all_apps_from_db: # Iterate through database apps
        app_required_role_names = {role.name for role in app.required_by_roles} # Get set of required role names
        # Check if user has at least one of the required roles for the app
        if user_role_names.intersection(app_required_role_names):
            # Convert to WebAppResponse object
            app_response = WebAppResponse(
                id=app.id,
                name=app.name,
                url=app.url,
                description=app.description,
                required_roles=list(app_required_role_names)
            )
            available_apps.append(app_response)

    return available_apps

# --- User Management Endpoints ---

# NEW: Endpoint to get the currently authenticated user's info
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Returns the details of the currently authenticated user.
    """
    return current_user

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Registers a new user in the system with specific roles. (Admin only)
    """
    # Check if username already exists
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the User object for the database (without roles initially)
    db_user = User(username=user.username, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user) # Refresh to get the auto-generated ID

    # Resolve and assign roles
    if user.roles:
        roles_to_assign = get_or_create_roles(session, user.roles)
        for role in roles_to_assign:
            db_user.roles.append(role)
    else:
        # Default to 'user' role if no roles specified
        default_role = session.exec(select(Role).where(Role.name == "user")).first()
        if default_role:
            db_user.roles.append(default_role)

    session.commit()
    session.refresh(db_user) # Refresh to get the updated relationships

    return db_user

@app.get("/users/", response_model=List[UserResponse])
async def read_users(
    offset: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Retrieves a list of all users with pagination and their associated roles. (Admin only)
    """
    # Ensure limit doesn't exceed 100
    limit = min(limit, 100)
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Retrieves a single user by their ID with their associated roles. (Admin only)
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Updates an existing user's information, including roles. (Admin only)
    Allows partial updates (e.g., just username, or just password, or just roles).
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Apply updates only for provided fields
    update_data = user_update.model_dump(exclude_unset=True) # Exclude fields that were not set in the request

    # Handle password separately
    if "password" in update_data:
        db_user.hashed_password = get_password_hash(update_data["password"])

    # Check for username conflict if username is being updated
    if "username" in update_data and update_data["username"] != db_user.username:
        existing_user = session.exec(select(User).where(User.username == update_data["username"])).first()
        if existing_user and existing_user.id != db_user.id: # Ensure it's not the current user
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already registered by another user"
            )
        db_user.username = update_data["username"]

    # Handle roles separately
    if "roles" in update_data:
        # Clear existing roles
        db_user.roles.clear()
        
        # Add new roles
        if update_data["roles"]:
            roles_to_assign = get_or_create_roles(session, update_data["roles"])
            for role in roles_to_assign:
                db_user.roles.append(role)

    session.commit()
    session.refresh(db_user) # Refresh to get latest state from DB

    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Deletes a user by their ID. (Admin only)
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    session.delete(user)
    session.commit()
    return {} # No content response for successful deletion

# NEW: WebApp CRUD Endpoints (Admin Only)

@app.post("/apps/", response_model=WebAppResponse, status_code=status.HTTP_201_CREATED)
async def create_webapp(
    webapp: WebAppCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Creates a new web application entry in the database with required roles. (Admin only)
    """
    db_webapp = session.exec(select(WebApp).where(WebApp.name == webapp.name)).first()
    if db_webapp:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Web application with this name already exists"
        )

    # Create the WebApp object for the database (without roles initially)
    db_webapp = WebApp(
        name=webapp.name, 
        url=webapp.url, 
        description=webapp.description
    )
    session.add(db_webapp)
    session.commit()
    session.refresh(db_webapp) # Refresh to get the auto-generated ID

    # Resolve and assign required roles
    if webapp.required_roles:
        roles_to_assign = get_or_create_roles(session, webapp.required_roles)
        for role in roles_to_assign:
            db_webapp.required_by_roles.append(role)
    else:
        # Default to 'user' role if no roles specified
        default_role = session.exec(select(Role).where(Role.name == "user")).first()
        if default_role:
            db_webapp.required_by_roles.append(default_role)

    session.commit()
    session.refresh(db_webapp) # Refresh to get the updated relationships

    return db_webapp

@app.get("/apps/{webapp_id}", response_model=WebAppResponse)
async def read_webapp_by_id(
    webapp_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Retrieves a single web application by its ID with its required roles. (Admin only)
    """
    webapp = session.get(WebApp, webapp_id)
    if not webapp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Web application not found"
        )
    return webapp

@app.patch("/apps/{webapp_id}", response_model=WebAppResponse)
async def update_webapp(
    webapp_id: int,
    webapp_update: WebAppUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Updates an existing web application's information, including required roles. (Admin only)
    Allows partial updates.
    """
    db_webapp = session.get(WebApp, webapp_id)
    if not db_webapp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Web application not found"
        )

    update_data = webapp_update.model_dump(exclude_unset=True)

    # Check for name conflict if name is being updated
    if "name" in update_data and update_data["name"] != db_webapp.name:
        existing_webapp = session.exec(select(WebApp).where(WebApp.name == update_data["name"])).first()
        if existing_webapp and existing_webapp.id != db_webapp.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Web application with this name already exists"
            )
        db_webapp.name = update_data["name"]

    # Update basic fields
    if "url" in update_data:
        db_webapp.url = update_data["url"]
    if "description" in update_data:
        db_webapp.description = update_data["description"]

    # Handle required_roles separately
    if "required_roles" in update_data:
        # Clear existing roles
        db_webapp.required_by_roles.clear()
        
        # Add new roles
        if update_data["required_roles"]:
            roles_to_assign = get_or_create_roles(session, update_data["required_roles"])
            for role in roles_to_assign:
                db_webapp.required_by_roles.append(role)

    session.commit()
    session.refresh(db_webapp)
    return db_webapp

@app.delete("/apps/{webapp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_webapp(
    webapp_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Deletes a web application from the database. (Admin only)
    """
    webapp = session.get(WebApp, webapp_id)
    if not webapp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Web application not found"
        )

    session.delete(webapp)
    session.commit()
    return {}

# JWT Utility Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Authenticates a user and returns an access token upon successful login.
    Now includes user's roles from database relationship in JWT.
    """
    # Fetch user with roles eager loaded
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Convert roles to comma-separated string for token
    user_role_names = [role.name for role in user.roles]
    roles_string = ",".join(user_role_names)
    access_token = create_access_token(
        data={"sub": user.username, "roles": roles_string},  # Store username and roles in token
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Role Management Endpoints ---

class RoleCreate(SQLModel):
    """Schema for creating a new role."""
    name: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)

class RoleUpdate(SQLModel):
    """Schema for updating an existing role."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)

class RoleResponse(SQLModel):
    """Schema for role responses."""
    id: int
    name: str
    description: Optional[str] = None
    
    model_config = {"from_attributes": True}

@app.get("/roles/", response_model=List[RoleResponse], dependencies=[Depends(get_current_admin_user)])
def get_all_roles(session: Session = Depends(get_session)):
    """
    Retrieves all roles in the system. (Admin only)
    """
    roles = session.exec(select(Role)).all()
    return roles

@app.post("/roles/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin_user)])
def create_new_role(role_create: RoleCreate, session: Session = Depends(get_session)):
    """
    Creates a new role. (Admin only)
    """
    # Check if role name already exists
    existing_role = session.exec(select(Role).where(Role.name == role_create.name)).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role name already exists"
        )
    
    db_role = Role(name=role_create.name, description=role_create.description)
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

@app.put("/roles/{role_id}", response_model=RoleResponse, dependencies=[Depends(get_current_admin_user)])
def update_existing_role(role_id: int, role_update: RoleUpdate, session: Session = Depends(get_session)):
    """
    Updates an existing role. (Admin only)
    """
    db_role = session.get(Role, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Check for name conflict if name is being updated
    update_data = role_update.model_dump(exclude_unset=True)
    if "name" in update_data and update_data["name"] != db_role.name:
        existing_role = session.exec(select(Role).where(Role.name == update_data["name"])).first()
        if existing_role and existing_role.id != db_role.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role name already exists"
            )
    
    # Apply updates
    for key, value in update_data.items():
        setattr(db_role, key, value)
    
    session.commit()
    session.refresh(db_role)
    return db_role

@app.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin_user)])
def delete_existing_role(role_id: int, session: Session = Depends(get_session)):
    """
    Deletes a role. (Admin only)
    Note: This will also remove the role from any users/apps that reference it.
    """
    db_role = session.get(Role, role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    # Optional: Check if role is in use and prevent deletion
    # You can add business logic here to prevent deletion of essential roles
    # or roles that are currently assigned to users/apps
    
    session.delete(db_role)
    session.commit()
    return


# --- Root and Catch-all Routes for Vue.js SPA ---
# IMPORTANT: These routes must be defined *after* all your API routes.

# --- Root and Catch-all Routes for Vue.js SPA ---
# IMPORTANT: These routes must be defined *after* all your API routes.

@app.get("/{full_path:path}", include_in_schema=False)
async def serve_vue_spa_catchall(full_path: str):
    """
    Serves the Vue.js SPA for any unmatched path.
    Excludes explicit API paths and serves static assets or index.html.
    """
    # Define API/Backend-specific prefixes that should NOT be handled by the SPA
    api_prefixes = ["token", "users", "apps", "roles", "docs", "openapi.json"]

    # Check if the requested path starts with any API prefix
    for prefix in api_prefixes:
        if full_path.startswith(prefix):
            raise HTTPException(status_code=404, detail=f"API path '{full_path}' not found or excluded from SPA routing.")

    # --- Attempt to serve a direct static file (JS, CSS, images, favicon etc.) ---
    # Construct the full path to the file *within the dist directory*
    file_path_in_dist = os.path.join("portal-frontend-vue/dist", full_path)

    # Check if the file actually exists and is a file
    if os.path.exists(file_path_in_dist) and os.path.isfile(file_path_in_dist):
        return FileResponse(file_path_in_dist)

    # --- Fallback to serving index.html for Vue Router ---
    # If no API path and no direct static file match, then it's a client-side route
    # (e.g., /apps, /admin/users). Serve index.html for Vue Router to handle.
    return FileResponse("portal-frontend-vue/dist/index.html")

# You can run this file to create the database and tables initially
# or it will be done automatically on app startup.
if __name__ == "__main__":
    print("This script is primarily meant to be run by Uvicorn.")
    print("To run the application, use: uvicorn main:app --reload")
    print("Creating database and tables for initial setup if not present...")
    create_db_and_tables()
