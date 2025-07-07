# Local Portal Backend

A FastAPI-based local portal backend with SQLModel for database operations and user management.

## Features

- FastAPI web framework
- SQLModel for database modeling (SQLite)
- User management with password hashing
- Role-based access control
- Automatic API documentation

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

## API Endpoints

### Base
- `GET /` - Welcome message
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### User Management (CRUD)
- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination: ?limit=N&offset=N)
- `GET /users/{user_id}` - Get a specific user by ID
- `PUT /users/{user_id}` - Update a user's details
- `DELETE /users/{user_id}` - Delete a user

### Features
- **Password Security**: All passwords are hashed using bcrypt
- **Input Validation**: Username (3-50 chars), password (6+ chars), roles
- **Unique Constraints**: Usernames must be unique
- **Error Handling**: Proper HTTP status codes and error messages
- **Pagination**: Configurable limits for user listings

## Database

The application uses SQLite with the following models:
- **User**: id, username, hashed_password, roles

## Testing

Run the comprehensive test script:
```bash
./test_api.sh
```

Or test individual endpoints manually:
```bash
# Create a user
curl -X POST "http://127.0.0.1:8000/users/" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "password123", "roles": "user"}'

# Get all users
curl "http://127.0.0.1:8000/users/"

# Get user by ID
curl "http://127.0.0.1:8000/users/1"

# Update user
curl -X PUT "http://127.0.0.1:8000/users/1" \
    -H "Content-Type: application/json" \
    -d '{"roles": "admin"}'

# Delete user
curl -X DELETE "http://127.0.0.1:8000/users/1"
```

## Development

The server runs on `http://127.0.0.1:8000` with auto-reload enabled for development.

## Next Steps

- Implement user CRUD operations ✅
- Add authentication endpoints
- Implement JWT token-based authentication
- Add role-based authorization middleware
