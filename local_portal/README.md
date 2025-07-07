# Local Portal Backend

A FastAPI-based user management system with SQLite database.

## Features

- User creation, reading, updating, and deletion
- Password hashing with bcrypt
- SQLite database with SQLModel ORM
- FastAPI with automatic API documentation
- Docker containerization for easy deployment

## Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### For Windows Users
- **Easy Start**: Double-click `start.bat`
- **See**: `WINDOWS_SETUP.md` for detailed Windows instructions

### For Linux/Mac Users
- **Easy Start**: Run `./docker.sh dev`
- **See**: `DOCKER_SETUP.md` for detailed setup instructions

### Running the Application

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd local_portal
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Development Mode

**Linux/Mac:**
```bash
./docker.sh dev
```

**Windows:**
```cmd
docker.bat dev
```

The `main.py` file is mounted as a volume, so changes will trigger auto-reload.

## Legacy Setup (Virtual Environment)

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
- **Docker Support**: Easy deployment with Docker and Docker Compose

### Example Usage

Create a user:
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123", "roles": "user"}'
```

## Database

The SQLite database is stored in the `./data/` directory and persisted between container restarts.

## Environment Variables

- `DATABASE_FILE`: Path to the SQLite database file (default: `database.db`)

## Production Deployment

For production, you may want to:

1. Remove the volume mount for `main.py` in `docker-compose.yml`
2. Use a proper reverse proxy (nginx configuration provided as example)
3. Set up proper environment variables
4. Use a more robust database (PostgreSQL, MySQL)
5. Implement proper authentication and authorization

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
