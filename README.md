# Full-Stack Todo Web Application

A modern, full-featured todo application built with Next.js 16+ (frontend) and FastAPI (backend), using Neon PostgreSQL for data persistence.

## 🎯 Features

- **User Authentication**: Secure signup, login, and session management with JWT tokens
- **Task Management**: Create, view, edit, delete, and mark tasks as complete
- **Real-time Updates**: Optimistic UI updates with automatic error handling
- **Responsive Design**: Mobile-first design that works seamlessly on all devices
- **Secure**: User data isolation, rate limiting, and comprehensive validation
- **Modern Stack**: Built with the latest technologies and best practices

## 🏗️ Architecture

This is a monorepo application with separate frontend and backend:

```
.
├── backend/          # FastAPI backend (Python 3.11+)
│   ├── main.py       # FastAPI app entry point
│   ├── models/       # SQLModel database models
│   ├── routes/       # API endpoint handlers
│   ├── services/     # Business logic
│   ├── auth/         # Authentication & JWT utilities
│   └── db.py         # Database configuration
│
├── frontend/         # Next.js 16+ frontend (React)
│   ├── app/          # App Router pages and layouts
│   ├── components/   # Reusable React components
│   ├── lib/          # Utilities, API client, types
│   └── public/       # Static assets
│
├── .env.example      # Environment variables template
├── package.json      # Root package.json with shared scripts
└── README.md         # This file
```

### Technology Stack

**Backend:**
- FastAPI - Modern, fast web framework for building APIs
- SQLModel - SQL toolkit with Pydantic models
- Neon PostgreSQL - Serverless PostgreSQL database
- JWT (python-jose) - Token-based authentication
- Uvicorn - ASGI server

**Frontend:**
- Next.js 16+ - React framework with App Router
- Better Auth - Authentication library
- Tailwind CSS - Utility-first CSS framework
- React Hook Form - Form management with validation
- Zod - TypeScript-first schema validation

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18.0 or higher
- **Python** 3.11 or higher
- **PostgreSQL** database (Neon recommended)

### 1. Clone and Setup

```bash
# Install root dependencies
npm install

# Setup Python virtual environment
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration:
# - DATABASE_URL: Your Neon PostgreSQL connection string
# - JWT_SECRET: Generate a secure random string
# - BETTER_AUTH_SECRET: Generate another secure random string
```

### 3. Initialize Database

```bash
cd backend
python init_db.py
```

### 4. Run Development Servers

```bash
# Start both backend and frontend (from root)
npm run dev

# Or start separately:
npm run dev:backend  # Backend on http://localhost:8000
npm run dev:frontend # Frontend on http://localhost:3000
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)

## 📦 Available Scripts

From the root directory:

```bash
npm run dev            # Start both backend and frontend in development
npm run build          # Build frontend for production
npm run start          # Start both backend and frontend in production
npm run test           # Run all tests (backend + frontend)
npm run lint           # Lint frontend code
npm run format         # Format all code (Python + JS/TS)
npm run clean          # Remove build artifacts and cache
```

Backend-specific (from `backend/`):

```bash
python -m uvicorn main:app --reload    # Start FastAPI dev server
pytest                                 # Run backend tests
black .                                # Format Python code
```

Frontend-specific (from `frontend/`):

```bash
npm run dev          # Start Next.js dev server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Lint code
npm run format       # Format code
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **Password Hashing**: Bcrypt with salt rounds=10
- **Rate Limiting**: 5 login attempts per 15 minutes per IP
- **User Isolation**: All database queries scoped by user_id
- **Input Validation**: Comprehensive validation on both frontend and backend
- **CORS Protection**: Configured CORS origins
- **SQL Injection Prevention**: Parameterized queries via SQLModel
- **XSS Protection**: Input sanitization and output encoding

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - Login and receive tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout and invalidate tokens

### Tasks
- `GET /api/v1/tasks` - Get all user tasks
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get task details
- `PUT /api/v1/tasks/{id}` - Update task
- `PATCH /api/v1/tasks/{id}/complete` - Toggle completion
- `DELETE /api/v1/tasks/{id}` - Delete task

### Health
- `GET /api/v1/health` - Health check endpoint

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# E2E tests (Playwright)
cd frontend
npx playwright test
```

## 📝 Environment Variables

See `.env.example` for all available environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT token signing
- `BETTER_AUTH_SECRET` - Secret key for Better Auth
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `RATE_LIMIT_ATTEMPTS` - Max login attempts
- `RATE_LIMIT_WINDOW_MINUTES` - Rate limit time window

## 🎨 UI Features

- **Responsive Design**: Mobile, tablet, and desktop layouts
- **Dark Mode Support**: Toggle between light and dark themes
- **Optimistic Updates**: Instant UI feedback with automatic rollback on error
- **Loading States**: Skeleton screens and spinners for better UX
- **Form Validation**: Real-time validation with helpful error messages
- **Accessibility**: WCAG AA compliant with keyboard navigation
- **Toast Notifications**: Feedback for all user actions

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ using Next.js, FastAPI, and Neon PostgreSQL
