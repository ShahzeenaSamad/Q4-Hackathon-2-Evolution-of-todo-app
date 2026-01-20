# Database Setup Guide for Todo App

This guide explains how to set up the PostgreSQL database for the Todo Web Application.

## Prerequisites

1. PostgreSQL database (local or cloud-hosted like Neon)
2. DATABASE_URL configured in `backend/.env`

## Database URL Format

### Local PostgreSQL:
```
DATABASE_URL=postgresql://user:password@localhost:5432/tododb
```

### Neon PostgreSQL (Recommended):
```
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Better Auth Compatible**: The users table follows Better Auth's expected schema with TEXT id and email fields.

### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Indexes

The following indexes are created for optimal query performance:

1. **idx_tasks_user_id**: For fast user-scoped queries
   ```sql
   CREATE INDEX idx_tasks_user_id ON tasks(user_id);
   ```

2. **idx_tasks_completed**: For filtering by completion status
   ```sql
   CREATE INDEX idx_tasks_completed ON tasks(completed);
   ```

3. **idx_tasks_created_at**: For reverse chronological ordering
   ```sql
   CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
   ```

## Foreign Key Constraints

- **fk_tasks_user_id**: Ensures referential integrity
  - `tasks.user_id REFERENCES users(id)`
  - `ON DELETE CASCADE`: Automatically deletes user's tasks when user is deleted

## Setup Instructions

### Option 1: Using Neon PostgreSQL (Recommended)

1. Create a free account at [Neon](https://neon.tech)
2. Create a new project and database
3. Copy the connection string
4. Update `backend/.env` with your DATABASE_URL
5. Run the initialization script (see below)

### Option 2: Using Local PostgreSQL

1. Install PostgreSQL on your system
2. Create a database:
   ```bash
   createdb tododb
   ```
3. Update `backend/.env` with your DATABASE_URL
4. Run the initialization script (see below)

## Running Database Initialization

### From Backend Directory:

```bash
cd backend

# Activate virtual environment (if not already active)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Run initialization script
python init_db.py
```

### Expected Output:

```
2026-01-17 10:00:00 - __main__ - INFO - Creating database tables...
2026-01-17 10:00:01 - __main__ - INFO - Database tables created successfully
2026-01-17 10:00:01 - __main__ - INFO - Created tables: users, tasks
2026-01-17 10:00:01 - __main__ - INFO - Created indexes: idx_tasks_user_id, idx_tasks_completed, idx_tasks_created_at
2026-01-17 10:00:01 - __main__ - INFO - Created constraints: uq_users_email, fk_tasks_user_id (CASCADE)

============================================================
Database initialization completed successfully!
============================================================

Tables created:
  - users (id, email, password_hash, name, created_at)
  - tasks (id, user_id, title, description, completed, created_at, updated_at)

Indexes created:
  - idx_tasks_user_id (for user-scoped queries)
  - idx_tasks_completed (for filtering by completion status)
  - idx_tasks_created_at (for reverse chronological ordering)

Constraints created:
  - uq_users_email (unique email constraint)
  - fk_tasks_user_id (foreign key with CASCADE delete)

============================================================
```

## Verifying Database Setup

### Using psql:

```bash
# Connect to your database
psql $DATABASE_URL

# List tables
\dt

# Describe users table
\d users

# Describe tasks table
\d tasks

# Check indexes
\di

# Exit
\q
```

### Using Python:

```python
from db import engine, check_db_connection

# Check connection
if check_db_connection():
    print("Database connection successful!")

# List tables
from sqlalchemy import inspect
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables: {tables}")
```

## Troubleshooting

### Connection Errors

**Error**: `connection to server at "localhost", port 5432 failed`

**Solution**:
- Ensure PostgreSQL is running
- Check that DATABASE_URL is correct
- Verify database exists

### Permission Errors

**Error**: `permission denied for database`

**Solution**:
- Check that the user in DATABASE_URL has CREATE TABLE permissions
- Grant permissions: `GRANT ALL PRIVILEGES ON DATABASE tododb TO your_user;`

### SSL Errors (Neon)

**Error**: `SSL connection required`

**Solution**:
- Ensure `?sslmode=require` is appended to your DATABASE_URL
- Example: `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`

## Security Notes

1. **Never commit .env file** to version control
2. **Use strong passwords** for database user
3. **Enable SSL** for cloud databases (Neon does this by default)
4. **Limit database user permissions** to only what's needed
5. **Use connection pooling** to prevent exhaustion (configured in db.py)

## Next Steps

After database initialization:

1. Start the backend server:
   ```bash
   cd backend
   python main.py
   ```

2. Test the health check endpoint:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

3. Expected response:
   ```json
   {
     "status": "healthy",
     "database": "connected",
     "version": "1.0.0"
   }
   ```

## Maintenance

### Backup Database (Neon):

Neon automatically creates backups. Check your Neon dashboard for restore options.

### Backup Database (Local):

```bash
pg_dump $DATABASE_URL > backup.sql
```

### Restore Database:

```bash
psql $DATABASE_URL < backup.sql
```

### Reset Database (Warning: Deletes All Data):

```python
from init_db import reset_database
reset_database()
```
