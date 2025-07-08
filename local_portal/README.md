# Local WebApp Portal

A secure, offline-first web application portal designed for local network users. This system allows administrators to manage user accounts and control access to various Dockerized web applications based on user roles and permissions.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Technologies Used](#3-technologies-used)
4. [Prerequisites](#4-prerequisites)
5. [Getting Started (Setup Guide)](#5-getting-started-setup-guide)
   * [Cloning the Repository](#cloning-the-repository)
   * [Initial Frontend Build](#initial-frontend-build)
   * [Docker Compose Setup](#docker-compose-setup)
   * [Initial Admin User Creation](#initial-admin-user-creation)
   * [Adding Sample Web Applications](#adding-sample-web-applications)
6. [Basic Management](#6-basic-management)
   * [Accessing the Portal](#accessing-the-portal)
   * [Login & Authentication](#login--authentication)
   * [Admin Dashboard](#admin-dashboard)
   * [User Management](#user-management)
   * [Web App Management](#web-app-management)
7. [Backup & Restore Guide](#7-backup--restore-guide)
   * [Database Backup](#database-backup)
   * [Database Restore (Recovery)](#database-restore-recovery)
   * [Automated Backup Scripts](#automated-backup-scripts)
8. [Developing and Integrating New Web Apps](#8-developing-and-integrating-new-web-apps)
   * [App Structure Template](#app-structure-template)
   * [Integration Steps](#integration-steps)
   * [Key Considerations for New Apps](#key-considerations-for-new-apps)
9. [Troubleshooting](#9-troubleshooting)
10. [Future Improvements (Ideas)](#10-future-improvements-ideas)
11. [License](#11-license)

---

## 1. Project Overview

The Local WebApp Portal provides a centralized entry point for users on a local network to access various web applications. It features a robust FastAPI backend for user and application management, a modern Vue.js frontend for a dynamic user interface, and leverages Docker Compose for easy deployment and orchestration of all services.

Key functionalities include:
* Secure user authentication using JWTs.
* Role-based access control for web applications.
* Admin UI to manage users (CRUD) and web application entries (CRUD).
* All web applications run in isolated Docker containers.
* Designed for offline use (once set up) within a local network.
* Comprehensive backup and restore capabilities.

## 2. Features

* **User Management:** Create, read, update, and delete user accounts with assigned roles.
* **Role-Based Access Control:** Assign multiple roles to users; define roles required for each web application.
* **Dynamic WebApp Listing:** The portal frontend dynamically displays web applications based on the logged-in user's roles, fetching app data from the database.
* **Secure Authentication:** Utilizes JWT (JSON Web Tokens) for stateless authentication.
* **Dockerized Services:** Backend, frontend, and all managed web applications run as isolated Docker containers.
* **Docker Compose Orchestration:** Simplifies multi-container application deployment and management.
* **Persistent Data:** User and app data in the SQLite database persists across container restarts using Docker volumes.
* **Automated Backup System:** Cross-platform scripts and dedicated Docker service for database backups.
* **Modern Frontend:** Interactive Single-Page Application (SPA) built with Vue.js.
* **Cross-Platform Support:** Works on Windows, Linux, and macOS.

## Project Architecture

### Frontend-Backend Integration

The portal uses a **Single-Page Application (SPA)** architecture where:

1. **Vue.js Frontend:** Built into static files (`dist/` directory) containing:
   - `index.html` - Main SPA entry point
   - `js/` - Compiled JavaScript bundles
   - `css/` - Compiled CSS styles  
   - `favicon.ico` - Site icon

2. **FastAPI Backend:** Serves both API endpoints and static files:
   - **API Routes:** `/users/*`, `/apps/*`, `/token`, `/docs` - handled by FastAPI
   - **Static Assets:** `/js/*`, `/css/*`, `/favicon.ico` - served directly from `dist/`
   - **SPA Routing:** All other routes serve `index.html` for Vue Router client-side routing

3. **Static File Serving Logic** (in `main.py`):
   ```python
   # Root route serves index.html
   @app.get("/")
   async def read_root():
       return FileResponse(os.path.join(static_dir, "index.html"))
   
   # Catch-all route for SPA and static files
   @app.get("/{full_path:path}")
   async def catch_all(full_path: str):
       # API routes return 404
       if full_path.startswith(("users", "apps", "token", "docs")):
           raise HTTPException(status_code=404)
       
       # Serve static files if they exist
       file_path = os.path.join(static_dir, full_path)
       if os.path.isfile(file_path):
           return FileResponse(file_path)
       
       # Otherwise serve index.html for SPA routing
       return FileResponse(os.path.join(static_dir, "index.html"))
   ```

This architecture ensures:
- Fast static asset delivery
- Proper SPA routing support  
- Clean separation between API and frontend routes
- No conflicts between Vue Router and FastAPI routing

## 3. Technologies Used

* **Backend:** Python 3.10+, FastAPI, SQLModel (for ORM), Passlib (for password hashing), Python-JOSE (for JWT).
* **Frontend:** Vue.js 3, Vue Router, Vuex (for state management), HTML, CSS.
* **Containerization:** Docker, Docker Compose.
* **Database:** SQLite (file-based, ideal for local deployment).
* **Sample WebApps:** Python 3.10+, Flask.
* **Backup System:** Cross-platform shell scripts (PowerShell for Windows, Bash for Linux).

## 4. Prerequisites

Before you begin, ensure you have the following installed on your host machine (Windows, Linux, or macOS):

* **Docker Desktop:** Essential for running Docker containers and Docker Compose.
  * [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
* **Node.js and npm (Node Package Manager):** Required to build the Vue.js frontend.
  * [Download Node.js](https://nodejs.org/en/download/) (npm is included with Node.js installation).
* **Git:** For cloning the repository.
  * [Download Git](https://git-scm.com/downloads)

## 5. Getting Started (Setup Guide)

Follow these steps to get the Local WebApp Portal up and running.

### Cloning the Repository

Open your terminal (Git Bash or PowerShell on Windows, any terminal on Linux/macOS) and clone the repository:

```bash
git clone <repository_url> # Replace <repository_url> with the actual URL of your project
cd local_portal
```

### Initial Frontend Build

Navigate into the Vue.js frontend directory and build its production assets. This dist folder will then be copied into the backend Docker image.

```bash
cd portal-frontend-vue
npm install       # Install frontend dependencies (only needed once or if package.json changes)
npm run build     # Compile Vue.js application into the 'dist' folder
cd ..             # Go back to the main 'local_portal' directory
```

**Troubleshooting npm install / npm run build:** If you encounter ERR_SOCKET_TIMEOUT or network errors, ensure your internet connection is stable. You might need to:
- Clear npm cache: `npm cache clean --force`
- Try a different npm registry: `npm config set registry https://registry.npmjs.org/`
- Temporarily disable firewall/VPN.

### Docker Compose Setup

This command will build all Docker images, set up the network, create a persistent volume for your database, and start all services.

1. **Create backups directory:** This folder will store your database backups on the host.

```bash
mkdir backups
```

2. **Spin up the entire stack:**

```bash
docker compose up --build -d
```

* `--build`: Ensures Docker images are (re)built. Use this if you change Dockerfiles or code within a service's build context.
* `-d`: Runs containers in detached mode (in the background).

This process will take some time on the first run as it downloads base images and installs dependencies within containers.

3. **Verify services are running:**

```bash
docker compose ps
```

You should see the `app` service running and healthy.

**Note:** The main portal service is named `app` in Docker Compose (not `portal-backend`). This service handles both the FastAPI backend and serves the Vue.js frontend static files through a unified static file serving system.

### Initial Admin User Creation

After the Docker Compose stack is up, you have two options for creating initial users:

**Option 1: Use the Sample Data Script (Recommended for Testing)**
```bash
docker compose exec app python /app/add_sample_webapps.py
```
This creates sample users, roles, and web applications for immediate testing. The admin user will be:
- Username: `admin`
- Password: `admin123`
- Roles: admin, user, project_manager, special_access, public

**Option 2: Manual Admin Creation via Swagger UI**
If you prefer to create your own admin user manually:

1. **Open Swagger UI:** Go to http://localhost:8000/docs

2. **Create an Admin User:**
   * Expand the `POST /users/` endpoint under "Users".
   * Click "Try it out".
   * In the "Request body", enter the details for your first admin user:

```json
{
  "username": "adminuser",
  "password": "your_secure_admin_password",
  "roles": ["admin", "user", "project_manager", "special_access"]
}
```

   * Choose a strong password!
   * Click "Execute". You should receive a `201 Created` response.

3. **Get Admin Access Token:**
   * Expand the `POST /token` endpoint under "Login".
   * Click "Try it out".
   * Enter the username (`adminuser`) and password you just created.
   * Click "Execute". You should receive a `200 OK` response with an `access_token`. Copy this entire `access_token` string.

4. **Authorize in Swagger UI:**
   * Click the "Authorize" button (a padlock icon usually at the top right of the Swagger UI).
   * In the "Value" field, type `Bearer ` (with a space) followed by your copied `access_token`.
   * Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbnVzZXIiLCJyb2xlcyI6ImFkbWluLCBlY2V0ZXJhIiwiaHR0cDo...`
   * Click "Authorize" then "Close". The padlock icon should now appear locked. You are now authorized to use the admin API endpoints.

### Adding Sample Web Applications

The portal includes a convenient script to populate the database with sample data, including users, roles, and web applications.

**Automated Sample Data Setup:**

```bash
# Run the sample data script inside the app container
docker compose exec app python /app/add_sample_webapps.py
```

This script will create:
- **Default Roles:** admin, user, project_manager, special_access, public
- **Sample Users:**
  - `admin` (password: `admin123`) - All roles including admin
  - `testuser` (password: `testpass`) - user, public roles
  - `manager` (password: `managerpass`) - user, project_manager, public roles
  - `specialuser` (password: `specialpass`) - user, special_access, public roles
- **Sample Web Applications:**
  - User Management Portal (admin only)
  - Simple User Dashboard (user, admin, public)
  - Admin Dashboard (admin only)
  - Project Management Tool (project_manager, admin, public)
  - Special Access Portal (special_access, admin)
  - Public Information Hub (public, user, admin)

**Manual Addition via Swagger UI:**

You can also add applications manually using the Swagger UI at http://localhost:8000/docs:

1. **Get Admin Access Token:**
   * Expand the `POST /token` endpoint under "Login".
   * Enter admin credentials and get the access token.
   * Click "Authorize" and enter `Bearer YOUR_TOKEN_HERE`.

2. **Add Web Application:**
   * Expand `POST /apps/` under "Webapp".
   * Example request body:

```json
{
  "name": "Simple User App",
  "url": "http://localhost:5001",
  "required_roles": ["user"],
  "description": "A basic application accessible to all standard users."
}
```

4. **Create a Regular User (Optional, but recommended for testing roles):**
   * Go to `POST /users/` again in Swagger UI.
   * Request body:

```json
{
  "username": "regularuser",
  "password": "regularpass123",
  "roles": ["user"]
}
```

   * Click "Execute".

## 6. Basic Management

### Quick Start Testing

After running the sample data script, you can immediately test the portal:

1. **Access the Portal:** http://localhost:8000
2. **Login with Admin Account:**
   - Username: `admin`
   - Password: `admin123`
3. **Test Admin Features:**
   - Click "Admin Dashboard" to access management views
   - Navigate to "User Management" to see all users
   - Navigate to "Role Management" to manage roles
   - Navigate to "WebApp Management" to see configured applications
4. **Test Regular User Access:**
   - Logout and login as `testuser` (password: `testpass`)
   - Should see only applications available to "user" role

### Accessing the Portal

Once all services are up, open your web browser and navigate to:

**http://localhost:8000**

This will load the Vue.js frontend login page.

**Technical Note:** The FastAPI backend (`main.py`) serves the Vue.js frontend using a sophisticated static file serving setup:
- Static assets (CSS, JS, favicon) are served directly from the `dist/` directory
- All non-API routes are served the Vue.js SPA `index.html` for client-side routing
- API routes (prefixed with `/users`, `/apps`, `/token`, `/docs`) are handled by FastAPI endpoints

### Login & Authentication

* **Login:** Enter your username and password on the login page.
* **Successful login** will redirect you to the "My Apps" page (`/apps`).
* **Logout:** Click the "Logout" link in the navigation bar. This clears your session token.

### Admin Dashboard

The "Admin Dashboard" link will only appear in the navigation bar if you are logged in as a user with the `admin` role.

* Clicking this link takes you to `http://localhost:8000/admin`.
* From here, you can navigate to "Manage Users" or "Manage WebApps".
* **Security:** Frontend route guards prevent non-admin users from accessing `/admin` paths directly, redirecting them to `/apps` and showing an access denied message.

**Admin UI Access Requirements:**
1. User must have `admin` role assigned
2. User must be successfully logged in with valid JWT token
3. Backend `/users/me` endpoint must return user data with admin role
4. Frontend Vuex store must receive and recognize admin role

**Troubleshooting Admin Access:**
- If admin dashboard link doesn't appear after login with admin user:
  1. Check browser console for errors
  2. Verify `/users/me` API call returns correct user data with admin role
  3. Check Vuex store state in Vue dev tools
  4. Ensure frontend was rebuilt after any backend changes: `npm run build`

### User Management

(Accessible via "Admin Dashboard" -> "Manage Users")

* **View Users:** Displays a table of all registered users, their IDs, usernames, and assigned roles.
* **Add New User:** Click "Add New User", fill out the form (username, password, roles as comma-separated list), and click "Add User".
* **Edit User:** Click "Edit" next to a user. A form will pre-populate. You can change their username, set a new password (leave blank to keep current), or modify their roles. Click "Update User".
* **Delete User:** Click "Delete" next to a user. A confirmation prompt will appear. Confirm to remove the user from the system.

### Web App Management

(Accessible via "Admin Dashboard" -> "Manage WebApps")

* **View Web Apps:** Displays a table of all registered web application entries, including their names, URLs, required roles, and descriptions.
* **Add New WebApp:** Click "Add New WebApp", fill out the form (name, URL, required roles, description), and click "Add WebApp".
* **Edit WebApp:** Click "Edit" next to an app. A form will pre-populate. You can change any of its details. Click "Update WebApp".
* **Delete WebApp:** Click "Delete" next to an app. Confirm to remove the web app entry from the system.

## 7. Backup & Restore Guide

The `database.db` file (containing all user and app configuration) is stored in a bind-mounted directory (`./data`) for persistence. This guide helps you back it up and restore it using the comprehensive backup system.

### Database Backup

A dedicated Docker Compose service (`backup-db`) is configured to copy your `database.db` file to a `backups` directory on your host machine.

#### Windows (PowerShell)

**Quick Backup (service keeps running):**
```powershell
.\scripts\windows\quick-backup.ps1
```

**Safe Backup (stops service temporarily):**
```powershell
.\scripts\windows\backup-database.ps1
```

**Interactive Management:**
```powershell
.\scripts\windows\backup-manager.ps1
```

#### Linux/macOS (Bash)

First, make scripts executable:
```bash
chmod +x scripts/linux/*.sh
```

**Quick Backup (service keeps running):**
```bash
./scripts/linux/quick_backup.sh
```

**Safe Backup (stops service temporarily):**
```bash
./scripts/linux/backup_db.sh
```

**Interactive Management:**
```bash
./scripts/linux/backup_manager.sh
```

#### Manual Docker Command

For any platform:
```bash
docker compose run --rm backup-db
```

### Database Restore (Recovery)

#### Windows (PowerShell)

```powershell
.\scripts\windows\restore-database.ps1
```

This script will:
1. Show available backup files
2. Let you select which backup to restore
3. Create a safety backup of your current database
4. Restore the selected backup
5. Restart services

#### Linux/macOS (Bash)

```bash
./scripts/linux/restore_db.sh
```

You can also specify a backup file directly:
```bash
./scripts/linux/restore_db.sh database_backup_20250107_143022.db
```

### Automated Backup Scripts

The portal includes comprehensive backup management:

#### Windows Scripts
- `scripts/windows/backup-database.ps1` - Safe backup with service management
- `scripts/windows/quick-backup.ps1` - Quick backup without stopping service
- `scripts/windows/restore-database.ps1` - Interactive restore with safety features
- `scripts/windows/cleanup-backups.ps1` - Manage old backup files
- `scripts/windows/backup-manager.ps1` - Menu-driven interface

#### Linux Scripts
- `scripts/linux/backup_db.sh` - Safe backup with service management
- `scripts/linux/quick_backup.sh` - Quick backup without stopping service
- `scripts/linux/restore_db.sh` - Interactive restore with safety features
- `scripts/linux/cleanup_backups.sh` - Manage old backup files
- `scripts/linux/backup_manager.sh` - Menu-driven interface
- `scripts/linux/setup_cron.sh` - Automated scheduling with cron

#### Automated Scheduling

**Windows (Task Scheduler):**
Use Windows Task Scheduler to run backup scripts automatically.

**Linux/macOS (Cron):**
```bash
# Set up daily backups at 3:00 AM
./scripts/linux/setup_cron.sh daily

# Set up weekly backups on Sunday at 2:30 AM
./scripts/linux/setup_cron.sh weekly

# Custom schedule
./scripts/linux/setup_cron.sh custom
```

## 8. Developing and Integrating New Web Apps

The portal is designed to manage any web application that can be Dockerized and exposed on a specific port.

### App Structure Template

For a new web app, follow a structure similar to `simple_user_app` or `admin_dashboard_app`. Each app needs:

- **A dedicated folder:** E.g., `my_new_webapp/`
- **app.py (or equivalent):** Your web application code, listening on a specific port (e.g., 5003).
- **requirements.txt:** List of Python dependencies for your app.
- **Dockerfile:** Instructions to build your app's Docker image.

#### Example `my_new_webapp/app.py` (Flask):

```python
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>My New WebApp</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background-color: #f8e1e1; text-align: center; }
            h1 { color: #8d021f; }
            p { color: #333; }
        </style>
    </head>
    <body>
        <h1>Welcome to My New Web Application!</h1>
        <p>This app is running on port 5003.</p>
        <p>You can go back to the <a href="http://localhost:8000">Portal</a>.</p>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)  # Listen on 5003
```

#### Example `my_new_webapp/requirements.txt`:

```
Flask==2.3.4
```

#### Example `my_new_webapp/Dockerfile`:

```dockerfile
FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5003  # Expose the port your app listens on
CMD ["python", "app.py"]
```

### Integration Steps

To integrate your new web app into the portal:

1. **Place the app folder:** Copy your `my_new_webapp` folder (containing `app.py`, `requirements.txt`, `Dockerfile`) into the `local_portal` root directory, alongside `simple_user_app` and `admin_dashboard_app`.

2. **Update docker-compose.yml:** Add a new service block for your app.

```yaml
# docker-compose.yml (excerpt)
services:
  # ... (existing app, simple-user-app, admin-dashboard-app, backup-db services) ...

  my-new-webapp:  # Choose a unique service name
    build:
      context: ./my_new_webapp  # Path to your new app's folder
    ports:
      - "5003:5003"  # Map host port 5003 to container port 5003
    networks:
      - portal_network
```

3. **Rebuild and Run Docker Compose:**
   You need to rebuild the Docker Compose stack to include your new service and its image.

```bash
docker compose up --build -d
```

4. **Add the App via Admin UI:**
   Once the `my-new-webapp` container is running:
   * Go to your portal: http://localhost:8000
   * Log in as an `adminuser`.
   * Go to "Admin Dashboard" -> "Manage WebApps".
   * Click "Add New WebApp".
   * Fill in the details:
     * **Name:** My New WebApp
     * **URL:** http://localhost:5003 (This is the URL your browser will use to access the app on your host machine)
     * **Required Roles:** E.g., `user` (or `new_role` if you want to define a specific role for it)
     * **Description:** A brief description.
   * Click "Add WebApp".

5. **Test:** Log out and log back in as a user with the required roles. "My New WebApp" should now appear in their list, and clicking "Launch App" should open it.

### Key Considerations for New Apps

* **Port Mapping** (`ports:` in docker-compose.yml): Ensure the `host_port:container_port` mapping is unique for each app on your host machine. The `container_port` must match the port your application is configured to listen on internally (e.g., `app.run(port=5003)`).

* **Internal Docker Network:** Within the docker-compose.yml network, services can communicate with each other using their service names (e.g., `app` could talk to `my-new-webapp` at `http://my-new-webapp:5003`). The frontend (browser) needs `localhost` with the host-mapped port.

* **Required Roles:** Carefully consider what roles should have access to your new application and add them to the `required_roles` list when adding the app via the Admin UI. New roles will be created in the database automatically when first assigned to a user or app.

* **Security:** Always consider security best practices for any web application you add, especially if it handles sensitive data or user input.

## 9. Troubleshooting

### Common Issues

## 9. Troubleshooting

### Common Issues

#### Frontend/Static Asset Issues

**"Unexpected token '<'" JavaScript Error (RESOLVED)**
This typically indicates the frontend is receiving HTML instead of JavaScript files.

*Symptoms:*
- Browser console shows syntax errors in JS files
- Vue.js application doesn't load properly
- Admin dashboard/management views not accessible

*Root Cause:* FastAPI static file serving configuration conflicts between `app.mount()` calls and catch-all routes.

*Solution (IMPLEMENTED):*
The current `main.py` uses a robust static file serving approach:

1. **Root Route:** Serves `index.html` for the main page (`/`)
2. **Catch-All Route:** Handles all other routes with this logic:
   ```python
   @app.get("/{full_path:path}")
   async def catch_all(full_path: str):
       # Skip API routes
       if full_path.startswith(("users", "apps", "token", "docs", "redoc")):
           raise HTTPException(status_code=404)
       
       # Serve static files if they exist
       file_path = os.path.join(static_dir, full_path)
       if os.path.isfile(file_path):
           return FileResponse(file_path)
       
       # Otherwise serve index.html for Vue Router
       return FileResponse(os.path.join(static_dir, "index.html"))
   ```

3. **No `app.mount()` Usage:** Removed problematic mount points that caused conflicts:
   ```python
   # These lines were REMOVED to fix the issue:
   # app.mount("/js", StaticFiles(directory=js_dir), name="js")
   # app.mount("/css", StaticFiles(directory=css_dir), name="css")
   # app.mount("/static", StaticFiles(directory=static_dir), name="static")
   ```

*If you still see this issue:*
1. Rebuild frontend: `cd portal-frontend-vue && npm run build && cd ..`
2. Rebuild containers: `docker compose up --build -d`
3. Check file serving in browser dev tools Network tab

**"TypeError: Cannot read properties of null" in Add Forms (RESOLVED)**
*Symptoms:*
- Clicking "Add New User" or "Add New WebApp" buttons causes JavaScript errors
- Browser console shows `TypeError: Cannot read properties of null (reading 'required_roles')` or similar
- Add forms don't appear or crash immediately

*Root Cause:* The add buttons were directly setting `showAddUserForm = true` or `showAddWebAppForm = true` without initializing the `selectedUser` or `selectedWebApp` objects. Since these start as `null`, the form components tried to access `null.required_roles` or `null.roles`.

*Solution (IMPLEMENTED):* 
1. **Changed button handlers** from direct assignment to method calls:
   ```vue
   <!-- Old (caused error): -->
   <button @click="showAddUserForm = true">Add New User</button>
   <button @click="showAddWebAppForm = true">Add New WebApp</button>
   
   <!-- New (fixed): -->
   <button @click="enterAddMode">Add New User</button>
   <button @click="enterAddMode">Add New WebApp</button>
   ```

2. **Added `enterAddMode` methods** to properly initialize objects:
   ```javascript
   // In UserManagementView.vue:
   enterAddMode() {
     this.selectedUser = { username: '', password: '', roles: [] };
     this.showAddUserForm = true;
     this.showEditUserForm = false;
     this.formMessage = '';
   }
   
   // In WebAppManagementView.vue:
   enterAddMode() {
     this.selectedWebApp = { name: '', url: '', required_roles: [], description: '' };
     this.showAddWebAppForm = true;
     this.showEditWebAppForm = false;
     this.formMessage = '';
   }
   ```

This ensures the form components always receive valid objects instead of `null` values.

**Admin Dashboard Not Visible After Login**
*Symptoms:*
- User logs in successfully but admin dashboard link doesn't appear
- Redirected to `/apps` page but admin features missing

*Root Cause:* Usually related to:
- Frontend not receiving correct user role information
- Backend `/users/me` endpoint not working properly
- Vuex state not updating with admin role

*Solution:*
1. Verify `/users/me` endpoint works:
   ```bash
   # Get token first, then test (replace TOKEN with actual token)
   curl -H "Authorization: Bearer TOKEN" http://localhost:8000/users/me
   ```

2. Check user has admin role in database:
   - Use Swagger UI at http://localhost:8000/docs
   - Use `GET /users/` endpoint with admin token
   - Confirm user has "admin" in roles array

3. Test frontend role detection:
   - Login and check browser dev tools Console for any JavaScript errors
   - Check Network tab for `/users/me` response
   - Should return user object with roles array containing "admin"

#### Docker Issues

**"Docker daemon is not running"**
- **Windows:** Start Docker Desktop
- **Linux:** `sudo systemctl start docker`
- **macOS:** Start Docker Desktop

**"Port already in use"**
```bash
# Check what's using the port
netstat -an | grep :8000  # Linux/macOS
netstat -an | findstr :8000  # Windows

# Stop conflicting services or change ports in docker-compose.yml
```

**Service fails to start with dependency errors**
```bash
# Check specific service logs
docker compose logs app

# Common Python dependency errors:
# - NameError: name 'get_current_active_admin_user' is not defined
#   Solution: Check main.py uses correct function name 'get_current_admin_user'
# - Import errors: Rebuild container with --build flag
docker compose up --build -d
```

#### Frontend Build Issues

**"npm install fails"**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json  # Linux/macOS
Remove-Item -Recurse -Force node_modules, package-lock.json  # PowerShell

npm install
```

**"npm run build fails"**
- Ensure Node.js version compatibility (14+ recommended)
- Check for syntax errors in Vue.js components
- Clear npm cache and retry

#### Service Health Issues

**Check service status:**
```bash
docker compose ps
docker compose logs app
```

**App service shows "unhealthy" status:**
1. Check logs for startup errors:
```bash
docker compose logs app
```

2. Common issues:
   - Port binding conflicts
   - Missing environment variables
   - Database connection issues
   - Python dependency errors

**Restart services:**
```bash
docker compose restart
```

**Full reset:**
```bash
docker compose down
docker compose up --build -d
```

#### Database/SQLModel Issues

**"ValueError: <class 'list'> has no matching SQLAlchemy type" Error**
*Symptoms:*
- Backend fails to start with SQLModel errors
- Database table creation fails
- Sample data script (`add_sample_webapps.py`) crashes

*Root Cause:* SQLModel relationship definitions using `Field(default_factory=list)` instead of proper `Relationship()` configuration.

*Solution:*
This error is typically caused by incorrect relationship definitions in SQLModel. The models in `main.py` use proper `Relationship()` definitions:

```python
# Correct (in main.py):
class Role(SQLModel, table=True):
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)
    web_apps: List["WebApp"] = Relationship(back_populates="required_by_roles", link_model=WebAppRoleLink)

# Incorrect (causes the error):
class Role(SQLModel, table=True):
    users: List["User"] = Field(default_factory=list)  # Wrong!
    web_apps: List["WebApp"] = Field(default_factory=list)  # Wrong!
```

If you see this error:
1. Rebuild the container: `docker compose up --build -d`
2. The latest version of `add_sample_webapps.py` handles relationships correctly using manual link table management

**Database Seeding Script Errors**

*"sqlite3.OperationalError: no such table: role"*
- The script now includes automatic table creation
- If you see this error, ensure the container is rebuilt: `docker compose up --build -d`

*"AttributeError: 'NoneType' object has no attribute '_sa_instance_state'"*
- Fixed in latest version by removing unnecessary `session.refresh()` calls
- Update script and rebuild: `docker compose up --build -d`

**Sample Data Script Usage**
```bash
# Clean database and re-seed (removes all existing data)
docker compose down -v  # -v removes database volume
docker compose up --build -d
docker compose exec app python /app/add_sample_webapps.py

# Add sample data to existing database (updates existing users/apps)
docker compose exec app python /app/add_sample_webapps.py
```

#### API/Backend Issues

**"404 Not Found" for API endpoints**
- Verify backend service is running: `docker compose ps`
- Check API documentation at http://localhost:8000/docs
- Ensure endpoints are correctly defined in `main.py`

**JWT Token Issues**
*Symptoms:*
- "Could not validate credentials" errors
- Automatic logout after login
- API calls returning 401 Unauthorized

*Solution:*
1. Clear browser local storage and cookies
2. Re-login to get fresh token
3. Check token expiration settings in backend

**CORS Issues**
*Symptoms:*
- Browser console shows CORS policy errors
- Frontend can't communicate with backend

*Solution:*
- Verify CORS middleware is properly configured in `main.py`
- Check allowed origins include frontend URL

### Debugging Steps

#### 1. Frontend Issues
```bash
# Check Vue.js build output
ls -la portal-frontend-vue/dist/

# Rebuild frontend
cd portal-frontend-vue
npm run build
cd ..

# Check browser console for errors
# Open browser dev tools (F12) and check Console tab
```

#### 2. Backend Issues
```bash
# Check backend logs
docker compose logs app

# Access backend container for debugging
docker compose exec app bash

# Test API directly
curl http://localhost:8000/docs
```

#### 3. Docker Network Issues
```bash
# Check Docker network
docker network ls
docker network inspect local_portal_portal_network

# Verify all services are on same network
docker compose ps
```

#### 4. Database Issues
```bash
# Check database file exists
ls -la data/

# Backup current database
docker compose run --rm backup-db

# Access database directly (SQLite)
docker compose exec app python -c "
from database import engine
from sqlmodel import SQLModel, Session, select
from models import User
with Session(engine) as session:
    users = session.exec(select(User)).all()
    for user in users:
        print(f'User: {user.username}, Roles: {user.roles}')
"
```

### Log Files

- **Application logs:** `docker compose logs app`
- **Individual service logs:** `docker compose logs [service_name]`
- **Backup logs (Linux):** `./backup_log.txt`
- **Real-time logs:** `docker compose logs -f app`

**Important Service Names:**
- Main portal (FastAPI + Vue.js): `app`
- Simple User App: `simple-user-app`  
- Admin Dashboard App: `admin-dashboard-app`
- Database backup service: `backup-db`

### Performance Issues

**Slow container startup:**
- Ensure sufficient disk space
- Check Docker Desktop resource allocation
- Restart Docker daemon

**High memory usage:**
- Monitor with `docker stats`
- Adjust Docker Desktop memory limits
- Consider container resource limits in docker-compose.yml

## 10. Future Improvements (Ideas)

### Enhanced Frontend UI
- More sophisticated styling and theming
- Better responsiveness for mobile devices
- Richer user experience for forms and tables
- Dark mode support

### Admin Features
- Role Management directly in the UI (CRUD for roles)
- Audit logging of admin actions
- User profiles/password change for regular users
- Bulk user operations

### Notifications & Monitoring
- Real-time feedback for operations (e.g., toast messages)
- System health monitoring dashboard
- Email notifications for critical events

### Security Enhancements
- Two-factor authentication (2FA)
- Session management improvements
- Rate limiting for API endpoints
- Enhanced password policies

### Production Hardening
- Container health checks
- Proper web server (Nginx/Gunicorn) setup for FastAPI
- Environment variable management for sensitive data
- SSL/TLS support
- Backup encryption

### Advanced Features
- Remote backup storage (AWS S3, FTP, etc.)
- Database replication
- High availability setup
- Container orchestration with Kubernetes

## 11. License

This project is open-source and available under the MIT License.

---

## Quick Reference

### Essential Commands

```bash
# Start the portal
docker compose up -d

# View services
docker compose ps

# View logs
docker compose logs app

# Add sample web applications
docker compose exec app python add_sample_webapps.py

# Rebuild frontend and restart (after Vue.js changes)
cd portal-frontend-vue && npm run build && cd .. && docker compose up --build -d

# Create backup (Windows)
.\scripts\windows\quick-backup.ps1

# Create backup (Linux)
./scripts/linux/quick_backup.sh

# Stop the portal
docker compose down

# Full rebuild
docker compose up --build -d
```

### Important URLs

- **Portal Frontend:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Simple User App:** http://localhost:5001
- **Admin Dashboard App:** http://localhost:5002

### Support

For issues, questions, or contributions, please refer to the project repository or contact the development team.
