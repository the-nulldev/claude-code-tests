# User Authentication API

A Flask-based RESTful API implementing JWT authentication with user registration, login, and protected routes.

## Features

- User registration with username and password
- Secure password hashing using bcrypt
- JWT-based authentication
- Protected routes requiring authentication
- SQLite database with SQLAlchemy ORM
- Comprehensive unit tests

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd claude-code-tests
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Development Mode

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Production Mode

```bash
export FLASK_ENV=production
export SECRET_KEY='your-secret-key-here'
export JWT_SECRET_KEY='your-jwt-secret-key-here'
python app.py
```

## API Endpoints

### Health Check
```
GET /
```

Returns API status and available endpoints.

### Register a New User
```
POST /register
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "johndoe"
  }
}
```

### Login
```
POST /login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "johndoe"
  }
}
```

### Get User Profile (Protected)
```
GET /profile
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Profile retrieved successfully",
  "user": {
    "id": 1,
    "username": "johndoe"
  }
}
```

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

Run with verbose output:
```bash
pytest -v
```

## Project Structure

```
.
├── app.py              # Main Flask application with routes
├── models.py           # Database models (User)
├── auth.py             # Authentication utilities and decorators
├── config.py           # Application configuration
├── requirements.txt    # Python dependencies
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # Test fixtures
│   └── test_auth.py    # Authentication tests
├── .gitignore
└── README.md
```

## Security Considerations

- Passwords are hashed using bcrypt before storage
- JWT tokens expire after 1 hour (configurable)
- Secret keys should be set via environment variables in production
- SQLite is suitable for development; use PostgreSQL/MySQL in production
- Always use HTTPS in production

## Configuration

Environment variables:
- `FLASK_ENV`: Set to `production` for production mode
- `SECRET_KEY`: Flask secret key for session management
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `DATABASE_URL`: Database connection string (default: SQLite)

## Testing Checklist

All acceptance criteria from the issue are met:

- [x] `/register` route to create a new user with username and password
- [x] `/login` route that authenticates a user and returns a token/session
- [x] Passwords are securely hashed using bcrypt
- [x] Protected route (`/profile`) that requires authentication
- [x] Unit tests for registration and login flows

## Example Usage with curl

### Register:
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Access Protected Route:
```bash
curl -X GET http://localhost:5000/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## License

MIT

---

Generated with [Claude Code](https://claude.ai/code)
