# User Management UI Testing Guide

## Overview
This guide will help you test the newly implemented User Management UI for the admin dashboard.

## Prerequisites
1. Docker Compose environment is running: `docker compose up -d`
2. You have an admin user in your database (typically `adminuser` with password `admin123`)

## Testing Steps

### 1. Login as Admin
1. Open your browser and navigate to `http://localhost:8000`
2. Login with admin credentials:
   - Username: `adminuser`
   - Password: `admin123`

### 2. Access Admin Dashboard
1. After successful login, you should see the main apps view
2. If you're logged in as an admin user, you'll see an "Admin Dashboard" button in the top navigation
3. Click on "Admin Dashboard" to access the admin interface

### 3. Navigate to User Management
1. In the Admin Dashboard, click on "Manage Users" 
2. You should be navigated to `/admin/users`

### 4. Test User Management Features

#### View Users
- You should see a table listing all users in the system
- Each user shows: ID, Username, Roles, and Actions (Edit/Delete)

#### Add New User
1. Click "Add New User" button
2. Fill out the form:
   - Username: `testuser3`
   - Password: `password123`
   - Roles: `user,project_manager` (comma-separated)
3. Click "Add User"
4. Verify: Success message appears and new user is added to the table

#### Edit Existing User
1. Click "Edit" next to any user
2. The form should populate with existing user data (password field will be empty for security)
3. Modify the roles (e.g., add `special_access` to a user's roles)
4. Optionally set a new password
5. Click "Update User"
6. Verify: Success message appears and changes are reflected in the table

#### Delete User
1. Click "Delete" next to a user (preferably a test user, not the admin)
2. Confirm the deletion in the prompt
3. Verify: Success message appears and user is removed from the table

### 5. Error Handling Tests

#### Test Unauthorized Access
1. Logout from the admin account
2. Login as a regular user (if you have one)
3. Try to access `/admin/users` directly
4. Verify: You should be redirected to the apps page (not allowed)

#### Test Invalid Operations
1. Try creating a user with an existing username
2. Try invalid role names
3. Verify: Appropriate error messages are displayed

## Expected UI Features

### Navigation
- Clean admin dashboard with navigation cards
- Breadcrumb-style navigation
- Admin-only access controls

### User Management Interface
- Modern table layout for user listing
- Inline forms for add/edit operations
- Responsive design elements
- Loading indicators during API calls
- Success/error message displays

### Form Features
- Username field disabled during edit (for security)
- Password field optional during edit
- Comma-separated roles input with clear labeling
- Form validation and error handling

## Troubleshooting

If you encounter issues:

1. **No admin access**: Ensure your user has the "admin" role in the database
2. **API errors**: Check browser developer tools network tab for detailed error messages
3. **Navigation issues**: Verify all components are properly built and Docker containers restarted
4. **Permission errors**: Ensure JWT token is valid and user has appropriate permissions

## Next Steps

After confirming user management works:
1. Test with different user roles
2. Verify role-based access to applications
3. Prepare for Web App Management implementation (similar pattern)

This completes the User Management UI implementation with full CRUD capabilities, proper authentication, and a modern, responsive interface.
