# Authentication Quick Start Guide

## Overview

This guide helps you quickly test the Phase 3 Authentication implementation (T023-T045).

**What's Implemented:**
- ✅ User registration with email/password
- ✅ Secure login with JWT tokens
- ✅ Automatic token refresh
- ✅ Session persistence
- ✅ Protected routes
- ✅ Rate limiting
- ✅ Password strength validation

---

## Prerequisites Check

Before testing, ensure you have:

1. **Python 3.10+** installed
2. **Node.js 18+** installed
3. **PostgreSQL database** (Neon recommended)
4. **Backend environment configured** (`backend/.env`)
5. **Frontend environment configured** (`frontend/.env.local`)

---

## Step 1: Setup Database

### Option A: Use Neon PostgreSQL (Recommended)

1. Go to [https://neon.tech](https://neon.tech)
2. Create a free account
3. Create a new project
4. Copy the connection string
5. Update `backend/.env`:
   ```bash
   DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```

### Option B: Use Local PostgreSQL

1. Install PostgreSQL locally
2. Create database:
   ```bash
   createdb tododb
   ```
3. Update `backend/.env`:
   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/tododb
   ```

---

## Step 2: Initialize Database Tables

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python init_db.py
```

**Expected output:**
```
✓ Database tables created successfully
  - users table
  - tasks table (for Phase 4)
```

---

## Step 3: Start Backend Server

```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test backend:**
- Open http://localhost:8000/api/v1/health
- Should see: `{"status":"healthy","database":"connected"}`
- Open http://localhost:8000/api/docs for API documentation

---

## Step 4: Run Backend Tests (Optional)

```bash
cd ..
python test_auth.py
```

**Tests:**
- ✓ Health check
- ✓ User signup
- ✓ User login
- ✓ Token refresh
- ✓ Protected endpoint
- ✓ Logout
- ✓ Rate limiting
- ✓ Password validation

---

## Step 5: Install Frontend Dependencies

```bash
cd frontend
npm install
```

**Expected output:**
```
added XXX packages in XXs
```

---

## Step 6: Start Frontend Server

```bash
npm run dev
```

**Expected output:**
```
▲ Next.js 15.1.4
- Local:        http://localhost:3000
```

---

## Step 7: Test Authentication Flow

### Test 1: User Signup

1. Navigate to **http://localhost:3000/signup**
2. Fill out the form:
   - **Email**: `test@example.com`
   - **Password**: `TestPass123!`
   - **Confirm Password**: `TestPass123!`
   - **Name** (optional): `Test User`
3. Observe password strength indicator (should show "Strong")
4. Click **"Create account"**
5. **Expected**: Redirects to `/login` with success message

### Test 2: User Login

1. Navigate to **http://localhost:3000/login**
2. Fill out the form:
   - **Email**: `test@example.com`
   - **Password**: `TestPass123!`
3. Click **"Sign in"**
4. **Expected**: Redirects to `/dashboard`

### Test 3: Protected Route

1. On `/dashboard`, verify you see:
   - Your email address
   - Your name
   - Your user ID
   - "Logout" button
2. **Refresh the page**
3. **Expected**: Still logged in (session persisted)

### Test 4: Logout

1. Click **"Logout"** button
2. **Expected**: Redirects to `/login`
3. Try accessing **http://localhost:3000/dashboard**
4. **Expected**: Redirects back to `/login` (protected route)

### Test 5: Automatic Token Refresh (Advanced)

1. Login again
2. Open browser **Developer Tools** → **Application** → **Local Storage**
3. Verify you see:
   - `refresh_token`
   - `user`
4. Wait 13+ minutes (access token expires in 15 min)
5. Click logout or navigate
6. **Expected**: Token auto-refreshed, no logout required

---

## Step 8: Test Security Features

### Test Rate Limiting

1. Go to **http://localhost:3000/login**
2. Enter wrong password 5 times
3. **Expected**: Error "Too many attempts. Please try again later."
4. Wait 15 minutes or use different IP

### Test Password Validation

1. Go to **http://localhost:3000/signup**
2. Try weak passwords:
   - `weak` → "Password must be at least 8 characters"
   - `password` → "Must contain uppercase, lowercase, digit, special"
   - `PASSWORD1` → "Must contain lowercase"
3. **Expected**: Clear error messages for each requirement

### Test Invalid Email

1. Go to **http://localhost:3000/signup**
2. Enter `invalid-email`
3. **Expected**: "Invalid email address"

---

## Step 9: Verify API Endpoints

### Using curl or Postman

**1. Health Check**
```bash
curl http://localhost:8000/api/v1/health
```

**2. Signup**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"api@example.com","password":"ApiPass123!","name":"API User"}'
```

**3. Login**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"api@example.com","password":"ApiPass123!"}'
```

**4. Get Current User** (requires access_token)
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**5. Refresh Token**
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"YOUR_REFRESH_TOKEN"}'
```

**6. Logout**
```bash
curl -X POST http://localhost:8000/api/v1/auth/logout
```

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
cd backend
pip install -r requirements.txt
```

**Issue**: `connection refused` or `database not connected`
- Check `DATABASE_URL` in `backend/.env`
- Verify PostgreSQL is running
- Run `python init_db.py` to create tables

**Issue**: Port 8000 already in use
```bash
# Change port in backend/.env
API_PORT=8001
```

### Frontend Issues

**Issue**: `Module not found: Can't resolve '@/lib/auth'`
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

**Issue**: CORS errors
- Check `CORS_ORIGINS` in `backend/.env`
- Ensure `NEXT_PUBLIC_API_URL` in `frontend/.env.local` matches backend

**Issue**: Port 3000 already in use
```bash
npm run dev -- -p 3001
```

### Authentication Issues

**Issue**: "Invalid credentials" on login
- Verify email is correct (case-insensitive)
- Verify password is correct
- Try signing up again (email might not exist)

**Issue**: "Session expired" immediately
- Check system time is correct
- Verify `JWT_SECRET` is set in `backend/.env`
- Clear browser localStorage and try again

**Issue**: Can't access `/dashboard`
- Verify you're logged in
- Check localStorage has `refresh_token` and `user`
- Open browser console for errors

---

## Environment Variables Reference

### Backend (`backend/.env`)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/tododb

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15
JWT_REFRESH_EXPIRATION_DAYS=7

# API
API_PORT=8000
API_HOST=0.0.0.0

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Rate Limiting
RATE_LIMIT_ATTEMPTS=5
RATE_LIMIT_WINDOW_MINUTES=15
```

### Frontend (`frontend/.env.local`)

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Better Auth (not currently used, using custom JWT)
BETTER_AUTH_SECRET=your-super-secret-better-auth-key-change-this
BETTER_AUTH_URL=http://localhost:3000
```

---

## Next Steps

Once authentication is working:

1. **Explore the Code**
   - `backend/auth/` - Authentication utilities
   - `backend/routes/auth.py` - Auth endpoints
   - `frontend/lib/auth.ts` - Auth hooks
   - `frontend/app/(auth)/` - Auth pages

2. **Proceed to Phase 4**
   - Task model and service
   - Task CRUD endpoints
   - Frontend task list and creation

3. **Security Hardening** (Phase 9)
   - Token blacklist
   - Email verification
   - Password reset flow

4. **UI Polish** (Phase 10)
   - Loading skeletons
   - Toast notifications
   - Responsive design

---

## Support

For issues or questions:

1. Check **PHASE_3_AUTH_COMPLETION_REPORT.md** for detailed documentation
2. Review **test_auth.py** for usage examples
3. Check browser console and terminal logs for errors
4. Verify all environment variables are set correctly

---

**Happy Testing! 🚀**
