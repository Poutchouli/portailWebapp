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

### Initial Admin User Creation

After the Docker Compose stack is up, you need to create an initial administrator user. This is done via the backend's API documentation (Swagger UI).

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

Using your authorized admin session in Swagger UI (http://localhost:8000/docs), add the sample web applications. These will appear in the portal based on user roles.

1. **Add "Simple User App":**
   * Expand `POST /apps/` under "Webapp".
   * Click "Try it out".
   * Request body:

```json
{
  "name": "Simple User App",
  "url": "http://localhost:5001",
  "required_roles": ["user"],
  "description": "A basic application accessible to all standard users."
}
```

   * Click "Execute". (201 Created response expected).

2. **Add "Admin Dashboard":**
   * Repeat the process for a second app.
   * Request body:

```json
{
  "name": "Admin Dashboard",
  "url": "http://localhost:5002",
  "required_roles": ["admin"],
  "description": "The administrative control panel, for administrators only."
}
```

   * Click "Execute". (201 Created response expected).

3. **(Optional) Add More Apps:** You can add additional apps like "Project Tracker" and "Sensitive Tool":

**Project Tracker:**
```json
{
  "name": "Project Tracker",
  "url": "http://localhost:8082",
  "required_roles": ["user", "project_manager"],
  "description": "Project management and tracking tools."
}
```

**Sensitive Tool:**
```json
{
  "name": "Sensitive Tool",
  "url": "http://localhost:8083",
  "required_roles": ["admin", "special_access"],
  "description": "High-security administrative tools."
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

### Accessing the Portal

Once all services are up, open your web browser and navigate to:

**http://localhost:8000**

This will load the Vue.js frontend login page.

### Login & Authentication

* **Login:** Enter your username and password on the login page.
* **Successful login** will redirect you to the "My Apps" page (`/apps`).
* **Logout:** Click the "Logout" link in the navigation bar. This clears your session token.

### Admin Dashboard

The "Admin Dashboard" link will only appear in the navigation bar if you are logged in as a user with the `admin` role.

* Clicking this link takes you to `http://localhost:8000/admin`.
* From here, you can navigate to "Manage Users" or "Manage WebApps".
* **Security:** Frontend route guards prevent non-admin users from accessing `/admin` paths directly, redirecting them to `/apps` and showing an access denied message.

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
.\quick-backup.ps1
```

**Safe Backup (stops service temporarily):**
```powershell
.\backup-database.ps1
```

**Interactive Management:**
```powershell
.\backup-manager.ps1
```

#### Linux/macOS (Bash)

First, make scripts executable:
```bash
chmod +x *.sh
```

**Quick Backup (service keeps running):**
```bash
./quick_backup.sh
```

**Safe Backup (stops service temporarily):**
```bash
./backup_db.sh
```

**Interactive Management:**
```bash
./backup_manager.sh
```

#### Manual Docker Command

For any platform:
```bash
docker compose run --rm backup-db
```

### Database Restore (Recovery)

#### Windows (PowerShell)

```powershell
.\restore-database.ps1
```

This script will:
1. Show available backup files
2. Let you select which backup to restore
3. Create a safety backup of your current database
4. Restore the selected backup
5. Restart services

#### Linux/macOS (Bash)

```bash
./restore_db.sh
```

You can also specify a backup file directly:
```bash
./restore_db.sh database_backup_20250107_143022.db
```

### Automated Backup Scripts

The portal includes comprehensive backup management:

#### Windows Scripts
- `backup-database.ps1` - Safe backup with service management
- `quick-backup.ps1` - Quick backup without stopping service
- `restore-database.ps1` - Interactive restore with safety features
- `cleanup-backups.ps1` - Manage old backup files
- `backup-manager.ps1` - Menu-driven interface

#### Linux Scripts
- `backup_db.sh` - Safe backup with service management
- `quick_backup.sh` - Quick backup without stopping service
- `restore_db.sh` - Interactive restore with safety features
- `cleanup_backups.sh` - Manage old backup files
- `backup_manager.sh` - Menu-driven interface
- `setup_cron.sh` - Automated scheduling with cron

#### Automated Scheduling

**Windows (Task Scheduler):**
Use Windows Task Scheduler to run backup scripts automatically.

**Linux/macOS (Cron):**
```bash
# Set up daily backups at 3:00 AM
./setup_cron.sh daily

# Set up weekly backups on Sunday at 2:30 AM
./setup_cron.sh weekly

# Custom schedule
./setup_cron.sh custom
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

#### Service Health Issues

**Check service status:**
```bash
docker compose ps
docker compose logs app
```

**Restart services:**
```bash
docker compose restart
```

**Full reset:**
```bash
docker compose down
docker compose up --build -d
```

#### Database Issues

**Database corruption:**
1. Stop services: `docker compose stop app`
2. Restore from backup using restore scripts
3. Start services: `docker compose start app`

**Missing database file:**
- The database will be created automatically on first run
- Create initial admin user via Swagger UI at http://localhost:8000/docs

### Log Files

- **Application logs:** `docker compose logs app`
- **Backup logs (Linux):** `./backup_log.txt`
- **Individual service logs:** `docker compose logs [service_name]`

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

# Create backup (Windows)
.\quick-backup.ps1

# Create backup (Linux)
./quick_backup.sh

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
