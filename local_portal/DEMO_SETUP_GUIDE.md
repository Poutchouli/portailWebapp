# Demo Setup Guide - Portal Web Application

## Overview
This guide will help you set up a complete working demo of the Portal Web Application on a new system using the provided database backup.

## Database Contents
The `DEMO_DATABASE_COMPLETE.db` file contains:
- **Sample Users:**
  - `admin` (password: `admin123`) - Full admin access with all roles
  - `testuser` (password: `testpass`) - Regular user with basic roles
  - `manager` (password: `managerpass`) - Project manager with extended permissions
  - `specialuser` (password: `specialpass`) - Special access user

- **Sample Roles:**
  - `admin` - Full administrative access
  - `user` - Basic user access
  - `project_manager` - Project management permissions
  - `special_access` - Special administrative tools
  - `public` - Public content access

- **Sample Web Applications:**
  - User Management Portal (admin only)
  - Simple User Dashboard (user, admin, public)
  - Admin Dashboard (admin only)
  - Project Management Tool (project_manager, admin, public)
  - Special Access Portal (special_access, admin)
  - Public Information Hub (public, user, admin)

## Prerequisites for New System
1. **Docker Desktop** installed and running
2. **Node.js 16+** and npm installed
3. **Git** for cloning the repository

## Setup Steps

### 1. Clone Repository
```bash
git clone <repository_url>
cd local_portal
```

### 2. Copy Database Backup
Place the `DEMO_DATABASE_COMPLETE.db` file in the project root directory.

### 3. Prepare Database Directory
```bash
# Create data directory
mkdir -p data

# Copy the demo database as the main database
cp DEMO_DATABASE_COMPLETE.db data/database.db
```

### 4. Build Frontend
```bash
cd portal-frontend-vue
npm install
npm run build
cd ..
```

### 5. Start with Docker Compose
```bash
docker compose up --build -d
```

### 6. Verify Setup
1. **Check container status:**
   ```bash
   docker compose ps
   ```
   You should see the `app` service running and healthy.

2. **Access the portal:**
   - Open browser to http://localhost:8000
   - You should see the login page

## Demo Walkthrough

### Admin User Testing
1. **Login as Admin:**
   - Username: `admin`
   - Password: `admin123`

2. **Explore Admin Features:**
   - Click "Admin Dashboard" in the navigation
   - Navigate to "User Management" to see all users
   - Navigate to "Role Management" to manage roles
   - Navigate to "WebApp Management" to manage applications

3. **Test User Management:**
   - Add a new user with various roles
   - Edit existing user roles
   - Delete test users (avoid deleting the admin user)

4. **Test WebApp Management:**
   - Add new web applications
   - Edit application URLs and required roles
   - Delete sample applications

### Regular User Testing
1. **Logout and login as regular user:**
   - Username: `testuser`
   - Password: `testpass`

2. **Verify Limited Access:**
   - Should only see applications available to "user" role
   - No admin dashboard access
   - Limited to basic functionality

### Project Manager Testing
1. **Login as project manager:**
   - Username: `manager`
   - Password: `managerpass`

2. **Verify Role-Based Access:**
   - Should see applications available to "project_manager" role
   - More access than regular user but less than admin

## Key Demo Features to Highlight

### 1. Role-Based Access Control
- Different users see different applications based on their roles
- Admin users have access to management interfaces
- Regular users have limited, role-appropriate access

### 2. Modern Admin Interface
- Full CRUD operations for users and web applications
- Real-time form validation and error handling
- Responsive design with modern UI components

### 3. Secure Authentication
- JWT-based authentication system
- Password hashing with bcrypt
- Session management and automatic logout

### 4. Single-Page Application Architecture
- Vue.js frontend with Vue Router for client-side routing
- FastAPI backend serving both API and static assets
- Clean separation between frontend and backend

### 5. Docker Containerization
- Complete application stack in Docker containers
- Easy deployment and scaling
- Persistent data storage with volume mounts

## Troubleshooting

### Container Issues
```bash
# Check logs
docker compose logs app

# Restart services
docker compose restart

# Full reset
docker compose down
docker compose up --build -d
```

### Database Issues
```bash
# Verify database file exists
ls -la data/database.db

# If missing, copy backup again
cp DEMO_DATABASE_COMPLETE.db data/database.db
```

### Frontend Issues
```bash
# Rebuild frontend
cd portal-frontend-vue
npm run build
cd ..
docker compose up --build -d
```

### Network Issues
- Ensure port 8000 is not being used by other applications
- Check Docker Desktop is running properly
- Verify firewall settings allow Docker networking

## Demo Script Suggestions

### 5-Minute Quick Demo
1. Show login with admin credentials
2. Navigate to User Management - show CRUD operations
3. Navigate to WebApp Management - demonstrate app configuration
4. Logout and login as regular user to show role restrictions
5. Highlight the responsive design and modern UI

### 15-Minute Detailed Demo
1. Architecture overview (Docker, Vue.js, FastAPI)
2. Admin functionality walkthrough
3. User role management demonstration
4. Web application configuration
5. Role-based access control demonstration
6. Security features (JWT, password hashing)
7. Docker deployment benefits
8. Q&A and customization possibilities

## Technical Highlights for Developers

- **Backend:** Python FastAPI with SQLModel ORM
- **Frontend:** Vue.js 3 with Vuex state management
- **Database:** SQLite with proper relationship modeling
- **Authentication:** JWT tokens with role-based permissions
- **Deployment:** Docker Compose with health checks
- **Static Serving:** Unified FastAPI static file serving for SPA
- **Security:** bcrypt password hashing, CORS configuration

## Next Steps After Demo

1. **Customization:** Adapt user roles and applications to specific needs
2. **Integration:** Connect to existing web applications and services
3. **Scaling:** Deploy to production with PostgreSQL or other databases
4. **Extensions:** Add features like user registration, password reset, audit logs
5. **Monitoring:** Implement logging, metrics, and health monitoring

This demo showcases a complete, production-ready web application portal with modern architecture, security best practices, and a professional user interface.
