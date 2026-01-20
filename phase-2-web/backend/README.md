# Backend - FastAPI Todo API

FastAPI backend for Phase II Todo App with JWT authentication and task CRUD operations.

## Features

- ✅ JWT Authentication
- ✅ Task CRUD Operations
- ✅ User Data Isolation
- ✅ PostgreSQL Database (SQLModel)
- ✅ API Documentation (Swagger/ReDoc)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Update `.env` with your values:

```env
DATABASE_URL=postgresql://username:password@host/database_name
JWT_SECRET=your-secret-key-min-32-characters-long
FRONTEND_URL=http://localhost:3000
```

### 3. Initialize Database

```python
from db import init_db
init_db()
```

Or run:

```bash
python -c "from db import init_db; init_db()"
```

## Running

### Development Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

API will be available at: http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/signup` | Create new user | No |
| POST | `/api/v1/auth/login` | Login user | No |
| POST | `/api/v1/auth/logout` | Logout user | Yes |
| GET | `/api/v1/auth/me` | Get current user | Yes |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/tasks` | List all tasks | Yes |
| POST | `/api/v1/tasks` | Create task | Yes |
| GET | `/api/v1/tasks/{id}` | Get task details | Yes |
| PUT | `/api/v1/tasks/{id}` | Update task | Yes |
| DELETE | `/api/v1/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/v1/tasks/{id}/complete` | Toggle completion | Yes |

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── models.py               # SQLModel database models
├── db.py                   # Database connection
├── auth.py                 # JWT authentication utilities
├── routes_auth.py          # Authentication endpoints
├── routes_tasks.py         # Task CRUD endpoints
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Testing

### Run Tests

```bash
pytest
```

### Manual Testing with cURL

**Signup:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securePassword123", "name": "John Doe"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securePassword123"}'
```

**Get Tasks:**
```bash
curl -X GET http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Deployment

### Environment Variables for Production

Set these in your hosting platform:

- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Strong secret key (min 32 characters)
- `FRONTEND_URL` - Your frontend URL (for CORS)

### Recommended Hosting

- Railway: https://railway.app
- Render: https://render.com
- Fly.io: https://fly.io

## Security

- ✅ JWT token required for all protected endpoints
- ✅ User data isolation at database level
- ✅ Password hashing with bcrypt
- ✅ CORS configured for frontend
- ✅ Input validation with Pydantic

## Troubleshooting

### Database Connection Error

```
Error: DATABASE_URL environment variable not set
```

**Solution:** Create `.env` file with `DATABASE_URL`

### JWT Error

```
Error: JWT_SECRET environment variable not set
```

**Solution:** Add `JWT_SECRET` to `.env` file

### Import Error

```
ModuleNotFoundError: No module named 'sqlmodel'
```

**Solution:** Install dependencies: `pip install -r requirements.txt`

---

**Status:** ✅ Backend implementation complete
**Phase:** Phase II - Full-Stack Web Application
