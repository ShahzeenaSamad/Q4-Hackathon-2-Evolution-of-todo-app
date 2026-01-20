# Feature: User Authentication

## Feature Overview

Implement secure user authentication using Better Auth on the frontend and JWT token verification on the backend to ensure each user can only access their own data.

---

## User Stories

### User Signup
**As a** new user
**I can** sign up with email and password
**So that** I can create my account and start using the app

### User Login
**As a** returning user
**I can** login with my email and password
**So that** I can access my tasks

### JWT Token Management
**As a** logged-in user
**I want** my session to persist securely
**So that** I don't have to login repeatedly

### User Data Isolation
**As a** user
**I want** to see only my own tasks
**So that** my data remains private

---

## Functional Requirements

### FR-1: User Signup

**Description:** New users can register with email and password.

**Input Fields:**
- `email` (string, required, valid email format)
- `password` (string, required, min 8 characters)
- `name` (string, optional, max 100 characters)

**Validation Rules:**
- Email must be valid format (RFC 5322)
- Email must be unique (no duplicate accounts)
- Password must be at least 8 characters
- Password is hashed before storage (bcrypt)
- Name is optional but max 100 characters if provided

**Business Rules:**
- Better Auth manages user creation in `users` table
- User session is created immediately after signup
- JWT token is issued and stored in HTTP-only cookie
- User is redirected to dashboard after successful signup

**Success Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123abc",
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2026-01-17T10:30:00Z"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**
```json
// Email already exists
{
  "success": false,
  "error": {
    "code": "EMAIL_EXISTS",
    "message": "An account with this email already exists"
  }
}

// Invalid email format
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format"
  }
}

// Password too short
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Password must be at least 8 characters"
  }
}
```

---

### FR-2: User Login

**Description:** Registered users can login with email and password.

**Input Fields:**
- `email` (string, required)
- `password` (string, required)

**Validation Rules:**
- Email must exist in database
- Password must match stored hash
- Account lockout after 5 failed attempts (optional)

**Business Rules:**
- Better Auth verifies credentials
- JWT token is issued upon successful authentication
- Token expires after 7 days
- Token is stored in HTTP-only cookie for security
- User is redirected to dashboard after login

**Success Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123abc",
      "email": "user@example.com",
      "name": "John Doe"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**
```json
// Invalid credentials
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}

// Account not found
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "No account found with this email"
  }
}
```

---

### FR-3: JWT Token Management

**Description:** JWT tokens are issued, stored, and sent with API requests.

**Token Payload:**
```json
{
  "sub": "user_123abc",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1737106200,
  "exp": 1737711000
}
```

**Token Configuration:**
- **Algorithm:** HS256 (HMAC-SHA256)
- **Secret:** Shared between frontend (Better Auth) and backend (FastAPI)
- **Expiration:** 7 days from issuance
- **Storage:** HTTP-only cookie (secure, sameSite)

**Environment Variables:**
```bash
# Frontend (.env.local)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-here

# Backend (.env)
JWT_SECRET=your-secret-key-here  # MUST MATCH FRONTEND
DATABASE_URL=postgresql://...
```

**Token Transmission:**
```
Frontend Request:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Backend Middleware:
1. Extract token from Authorization header
2. Verify signature with JWT_SECRET
3. Decode payload to get user_id
4. Attach user_id to request.state
```

---

### FR-4: JWT Verification Middleware

**Description:** Backend middleware verifies JWT on every protected request.

**Implementation:**
```python
from fastapi import Request, HTTPException
from jose import jwt, JWTError

async def verify_jwt(request: Request):
    # Extract token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid authorization header")

    token = auth_header.split(" ")[1]

    # Verify token
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")

        # Attach to request state
        request.state.user_id = user_id

    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
```

**Usage in Routes:**
```python
@app.get("/api/v1/tasks", dependencies=[Depends(verify_jwt)])
async def get_tasks(request: Request):
    user_id = request.state.user_id
    # Fetch tasks for this user only
```

---

### FR-5: User Data Isolation

**Description:** All database queries are filtered by `user_id`.

**Implementation Pattern:**
```python
# WRONG - Returns all tasks (INSECURE!)
def get_all_tasks():
    return session.query(Task).all()

# CORRECT - Returns only user's tasks (SECURE)
def get_user_tasks(user_id: str):
    return session.query(Task).filter(Task.user_id == user_id).all()
```

**Applied To:**
- ✅ List tasks (WHERE user_id = ?)
- ✅ Create task (SET user_id = ?)
- ✅ Get task (WHERE user_id = ? AND id = ?)
- ✅ Update task (WHERE user_id = ? AND id = ?)
- ✅ Delete task (WHERE user_id = ? AND id = ?)

**Error Handling:**
```python
# User tries to access another user's task
task = session.query(Task).filter(
    Task.id == task_id,
    Task.user_id == user_id
).first()

if not task:
    # Could be "not found" OR "belongs to different user"
    raise HTTPException(404, "Task not found")
```

**Security Benefit:** Users cannot discover or access other users' tasks by guessing IDs.

---

### FR-6: Logout

**Description:** Users can logout and invalidate their session.

**Implementation:**
- Better Auth clears the HTTP-only cookie
- JWT token remains valid until expiration (stateless)
- Optional: Implement token blacklist for immediate invalidation

**Frontend:**
```typescript
await auth.signOut();
redirect("/login");
```

**Success Response:**
```json
{
  "success": true,
  "data": {
    "message": "Logged out successfully"
  }
}
```

---

## Non-Functional Requirements

### NFR-1: Security
- ✅ Passwords hashed with bcrypt (cost factor: 10)
- ✅ JWT tokens signed with HS256
- ✅ HTTPS required in production
- ✅ HTTP-only cookies prevent XSS
- ✅ SameSite cookies prevent CSRF
- ✅ Token expiration: 7 days
- ✅ Secret key at least 32 characters

### NFR-2: Performance
- ✅ Login response < 500ms
- ✅ Signup response < 500ms
- ✅ JWT verification < 50ms
- ✅ Database queries indexed by user_id

### NFR-3: Usability
- ✅ Clear error messages
- ✅ Remember me option (extend token to 30 days)
- ✅ Password reset flow (future enhancement)
- ✅ Email verification (future enhancement)

---

## UI Requirements

### Login Page

**Location:** `@specs/ui/pages.md#login-page`

**Features:**
- Email input field
- Password input field (with show/hide toggle)
- "Remember me" checkbox
- Login button (loading state)
- "Don't have an account? Sign up" link
- Error message display
- Form validation feedback

### Signup Page

**Location:** `@specs/ui/pages.md#signup-page`

**Features:**
- Email input field
- Password input field (with show/hide toggle)
- Confirm password field
- Name input field (optional)
- Signup button (loading state)
- "Already have an account? Login" link
- Password strength indicator
- Error message display
- Form validation feedback

### Auth Layout

**Location:** `@specs/ui/pages.md#auth-layout`

**Features:**
- Centered card layout
- App logo/branding
- Responsive design (mobile-friendly)
- Background styling

---

## Database Schema

**Detailed Specification:** `@specs/database/schema.md#users-table`

**Table Structure:**
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,           -- UUID from Better Auth
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    emailVerifiedAt TIMESTAMP,
    image TEXT,                     -- Profile image URL
    createdAt TIMESTAMP DEFAULT NOW(),
    updatedAt TIMESTAMP DEFAULT NOW()
);

-- Better Auth may also create these tables:
-- sessions (for session management)
-- accounts (for OAuth providers)
-- verificationTokens (for email verification)
```

**Better Auth Integration:**
```typescript
// Better Auth schema adapter
import { betterAuth } from "better-auth"
import { prismaAdapter } from "better-auth/adapters/prisma"

export const auth = betterAuth({
  database: prismaAdapter(prisma),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false  // Optional for Phase II
  },
  JWT: {
    enabled: true,
    expiresIn: "7d"
  }
})
```

---

## API Endpoints

**Detailed Specification:** `@specs/api/rest-endpoints.md#authentication`

**Authentication Endpoints:**

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/api/v1/auth/signup` | No | Create new user |
| POST | `/api/v1/auth/login` | No | Login user |
| POST | `/api/v1/auth/logout` | Yes | Logout user |
| GET | `/api/v1/auth/me` | Yes | Get current user info |

**Note:** Better Auth may create its own endpoints like `/api/auth/sign-in`, `/api/auth/sign-out`, etc.

---

## Security Considerations

### SC-1: Password Security
- ✅ Hashed with bcrypt (never store plaintext)
- ✅ Minimum 8 characters
- ✅ Optional: Password complexity requirements
- ✅ Optional: Password strength meter

### SC-2: Token Security
- ✅ Signed with HS256 algorithm
- ✅ Secret key stored in environment variable
- ✅ Secret key at least 32 characters
- ✅ Token expiration: 7 days
- ✅ HTTP-only cookies prevent XSS

### SC-3: Data Isolation
- ✅ Every query filtered by user_id
- ✅ User cannot bypass with URL manipulation
- ✅ 404 error for other users' resources (prevents enumeration)

### SC-4: HTTPS
- ✅ Required in production
- ✅ Prevents token interception
- ✅ Vercel provides automatic HTTPS

### SC-5: Common Vulnerabilities
- ✅ SQL Injection prevented by ORM
- ✅ XSS prevented by React escaping
- ✅ CSRF prevented by SameSite cookies
- ✅ Session fixation prevented by token regeneration

---

## Acceptance Criteria

### AC-1: User Signup
- ✅ User can signup with valid email and password
- ✅ System rejects invalid email format
- ✅ System rejects password < 8 characters
- ✅ System rejects duplicate email
- ✅ User is created in database
- ✅ JWT token is issued
- ✅ User is redirected to dashboard

### AC-2: User Login
- ✅ User can login with correct credentials
- ✅ System rejects incorrect credentials
- ✅ System shows clear error message
- ✅ JWT token is issued
- ✅ User is redirected to dashboard

### AC-3: JWT Verification
- ✅ Valid token is accepted
- ✅ Invalid token is rejected with 401
- ✅ Expired token is rejected with 401
- ✅ Missing token is rejected with 401
- ✅ user_id is extracted from token

### AC-4: Data Isolation
- ✅ User can only see their own tasks
- ✅ User cannot access other users' tasks
- ✅ 404 error for other users' resources
- ✅ All CRUD operations respect user_id

### AC-5: Logout
- ✅ User can logout successfully
- ✅ Cookie is cleared
- ✅ User is redirected to login
- ✅ Protected routes require login again

---

## Edge Cases

### EC-1: Token Expiration
**Scenario:** User's token expires while using app
**Handling:** Redirect to login with message "Session expired, please login again"

### EC-2: Concurrent Login
**Scenario:** User logs in from multiple devices
**Handling:** Allowed (each device gets its own token)

### EC-3: Password Reset
**Scenario:** User forgets password
**Handling:** Not implemented in Phase II (future enhancement)

### EC-4: Email Verification
**Scenario:** User signs up but doesn't verify email
**Handling:** Not required for Phase II (optional)

### EC-5: Account Lockout
**Scenario:** User enters wrong password 5 times
**Handling:** Optional (not implemented in Phase II)

---

## Testing Requirements

### Unit Tests
- ✅ Password hashing function
- ✅ JWT generation function
- ✅ JWT verification function
- ✅ User ID extraction

### Integration Tests
- ✅ Signup endpoint
- ✅ Login endpoint
- ✅ Logout endpoint
- ✅ JWT middleware
- ✅ Data isolation (user A cannot access user B's data)

### E2E Tests
- ✅ Complete signup flow
- ✅ Complete login flow
- ✅ Protected page access (redirect to login)
- ✅ Logout flow

---

## Related Specifications

- **Overview:** `@specs/overview.md`
- **Architecture:** `@specs/architecture.md`
- **Features:** `@specs/features/task-crud.md`
- **API:** `@specs/api/rest-endpoints.md`
- **Database:** `@specs/database/schema.md`
- **UI:** `@specs/ui/pages.md`

---

**Document Status:** ✅ Ready for Review
**Last Updated:** January 17, 2026
**Phase:** Phase II - Full-Stack Web Application
