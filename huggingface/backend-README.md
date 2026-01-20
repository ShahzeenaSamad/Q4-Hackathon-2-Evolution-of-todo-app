---
title: TaskFlow API
emoji: ⚡
colorFrom: #5C8374
colorTo: #1B4242
sdk: docker
pinned: false
license: mit
---

# TaskFlow Backend API

FastAPI backend for TaskFlow todo application.

## 🚀 Features

- 🔐 JWT authentication with refresh tokens
- 📊 RESTful API design
- 🗄️ PostgreSQL database with SQLAlchemy
- 🚀 High performance async operations
- 📝 Comprehensive API documentation (auto-generated)

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (HS256)

## 📦 Required Environment Variables

Configure these in your Space settings:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
JWT_REFRESH_EXPIRATION_DAYS=7

# Server Configuration
PORT=7860
HOST=0.0.0.0
CORS_ORIGINS=https://your-frontend-space.hf.space
```

## 🔒 Security Notes

- Generate `JWT_SECRET` using: `openssl rand -hex 32`
- Use a production PostgreSQL database (Neon, Supabase, etc.)
- Add your frontend Space URL to `CORS_ORIGINS`

## 📖 API Documentation

Once deployed, visit:
- **Swagger UI**: `https://your-space.hf.space/docs`
- **ReDoc**: `https://your-space.hf.space/redoc`

## 📝 License

MIT License
