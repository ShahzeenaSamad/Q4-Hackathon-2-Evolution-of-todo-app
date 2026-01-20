# Quick Start Guide - Phase 2 Foundation

## Prerequisites Checklist

Before starting, ensure you have:

- [x] Python 3.10+ installed
- [x] Node.js 20+ installed
- [x] Git installed
- [ ] PostgreSQL database (Neon recommended - see DATABASE_SETUP.md)
- [ ] DATABASE_URL configured in `backend/.env`

---

## Database Setup (ONE-TIME SETUP)

### Option 1: Neon PostgreSQL (Recommended - Free)

1. Go to https://neon.tech and sign up
2. Create a new project
3. Copy the connection string
4. Update `backend/.env`:
   ```env
   DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```

### Option 2: Local PostgreSQL

1. Install PostgreSQL locally
2. Create database:
   ```bash
   createdb tododb
   ```
3. Update `backend/.env`:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/tododb
   ```

### Initialize Database Tables

```bash
cd backend
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac
python init_db.py
```

Expected output:
```
============================================================
Database initialization completed successfully!
============================================================
```

---

## Starting Development Servers

### Terminal 1: Backend Server

```bash
cd backend

# Activate virtual environment
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Start backend server
python main.py
```

Backend starts at: **http://localhost:8000**

### Terminal 2: Frontend Server

```bash
cd frontend

# Start frontend server
npm run dev
```

Frontend starts at: **http://localhost:3000**

---

## Verification

### 1. Test Backend Health

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### 2. Test Frontend Loads

Open browser: **http://localhost:3000**

Should see: "Todo App" heading with "Phase 2 Foundation Complete"

### 3. Test Database Tables

```bash
cd backend
.venv/Scripts/python
```

```python
from db import engine
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables: {tables}")  # Should show: ['users', 'tasks']
exit()
```

---

## Available Endpoints

### Backend API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Current Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API info |
| GET | `/api/v1/health` | Health check with database status |

---

## Development Workflow

### Making Changes

**Backend**:
- Edit files in `backend/`
- FastAPI auto-reloads on save (hot reload)
- Changes appear immediately at http://localhost:8000

**Frontend**:
- Edit files in `frontend/` or `frontend/app/`
- Next.js auto-reloads on save (fast refresh)
- Changes appear immediately at http://localhost:3000

### Linting & Formatting

**Backend**:
```bash
cd backend
.venv/Scripts/activate

# Lint with ruff
ruff check .

# Format with black
black .

# Type check with mypy
mypy .
```

**Frontend**:
```bash
cd frontend

# Lint
npm run lint

# Format
npm run format
```

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Database connection failed**:
- Verify DATABASE_URL in `backend/.env`
- Check database server is running
- Test connection: `python -c "from db import check_db_connection; print(check_db_connection())"`

### Frontend Issues

**Port 3000 already in use**:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

**Module not found errors**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Environment Variables Reference

### Backend (.env)

```env
# Database (REQUIRED - configure before running)
DATABASE_URL=postgresql://user:password@localhost:5432/tododb

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
JWT_REFRESH_EXPIRATION_DAYS=7

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend (.env.local)

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-super-secret-better-auth-key-change-this
BETTER_AUTH_URL=http://localhost:3000

# Frontend Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Next Steps

After Phase 2 foundation is complete and database is configured:

1. **Phase 3**: Implement User Story 1 (Authentication)
   - User registration and login
   - JWT token management
   - Protected routes

2. **Phase 4**: Implement User Story 2 (Create/View Tasks)
   - Task creation form
   - Task list display
   - Task CRUD operations

See `tasks.md` for complete task breakdown.

---

## Useful Commands

```bash
# Backend
cd backend && .venv/Scripts/activate && python main.py

# Frontend
cd frontend && npm run dev

# Database init
cd backend && .venv/Scripts/activate && python init_db.py

# Check health
curl http://localhost:8000/api/v1/health

# View logs
# Backend logs appear in terminal
# Frontend logs appear in terminal and browser console
```

---

**Documentation**:
- Full setup guide: `backend/DATABASE_SETUP.md`
- Phase 2 completion report: `phase-2-web/PHASE_2_COMPLETION_REPORT.md`
- Task breakdown: `phase-2-web/tasks.md`
- Implementation plan: `phase-2-web/plan.md`

**Support**:
- FastAPI docs: https://fastapi.tiangolo.com
- Next.js docs: https://nextjs.org/docs
- SQLModel docs: https://sqlmodel.tiangolo.com
