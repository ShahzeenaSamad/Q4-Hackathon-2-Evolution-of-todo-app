# Skill: API Testing

## Metadata

**Skill Name:** `api-testing`

**Description:** Test REST APIs using Swagger or Postman. Validate auth, CRUD operations, and error handling.

**Version:** 1.0

**Author:** Claude Code

**Created:** January 17, 2026

---

## Purpose

This skill validates REST API implementations by:
- Testing authentication flows (signup, login, JWT verification)
- Validating CRUD operations (Create, Read, Update, Delete)
- Testing error handling and validation
- Checking API responses and status codes
- Verifying data isolation and user data privacy

---

## When to Use

Use this skill when:
- Backend API implementation is complete
- API endpoints need validation
- Testing authentication and authorization
- Validating CRUD operations
- Checking error responses
- Postman/Swagger test creation
- API documentation verification

**Prerequisites:**
- FastAPI backend running
- Database initialized
- Environment variables configured
- API specifications approved

---

## Core Principles

1. **Comprehensive Testing:** Test all endpoints systematically
2. **Security Testing:** Verify authentication and authorization
3. **Data Isolation:** Ensure users can only see their own data
4. **Error Validation:** Verify error handling works correctly
5. **Documentation:** Create test documentation for reuse

---

## Testing Strategy

### Test Categories

#### 1. Authentication Tests

**Signup Endpoint:**
```bash
# Test 1: Valid signup
POST /api/v1/auth/signup
Content-Type: application/json
Body:
{
  "email": "test@example.com",
  "password": "testPassword123",
  "name": "Test User"
}

Expected: 201 Created
Response:
{
  "success": true,
  "data": {
    "user": {...},
    "token": "eyJhbGci..."
  }
}
```

**Login Endpoint:**
```bash
# Test 2: Valid login
POST /api/v1/auth/login
Content-Type: application/json
Body:
{
  "Email": "test@example.com",
  "password": "testPassword123"
}

Expected: 200 OK
Response:
{
  "success": true,
  "data": {
    "user": {...},
    "token": "eyJhbGci..."
  }
}
```

**Invalid Login:**
```bash
# Test 3: Invalid credentials
POST /api/v1/auth/login
Content-Type: application/json
Body:
{
  "email": "wrong@example.com",
  "password": "wrongpassword"
}

Expected: 401 Unauthorized
Response:
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

#### 2. Task CRUD Tests

**Create Task:**
```bash
# Test 4: Create task (with valid JWT)
POST /api/v1/tasks
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>
Body:
{
  "title": "Test Task",
  "description": "Test Description"
}

Expected: 201 Created
Response:
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Test Task",
    "description": "Test Description",
    "user_id": "user_123",
    "completed": false,
    "created_at": "2026-01-17T..."
  }
}
```

**Get Tasks:**
```bash
# Test 5: List all tasks
GET /api/v1/tasks
Authorization: Bearer <JWT_TOKEN>

Expected: 200 OK
Response:
{
  "success": true,
  "data": {
    "tasks": [...],
    "pagination": {...}
  }
}
```

**Get Single Task:**
```bash
# Test 6: Get task by ID
GET /api/v1/tasks/1
Authorization: Bearer <JWT_TOKEN>

Expected: 200 OK
Response:
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Test Task",
    ...
  }
}
```

**Update Task:**
```bash
# Test 7: Update task
PUT /api/v1/tasks/1
Authorization: Bearer <JWT_TOKEN>
Body:
{
  "title": "Updated Task Title"
}

Expected: 200 OK
Response:
{
  "success": True,
  "data": {
    "id": 1,
    "title": "Updated Task Title",
    ...
  }
}
```

**Toggle Complete:**
```bash
# Test 8: Toggle task completion
PATCH /api/v1/tasks/1/complete
Authorization: Bearer <JWT_TOKEN>

Expected: 200 OK
Response:
{
  "success": True,
  "data": {
    "id": 1,
    "completed": true,
    ...
  }
}
```

**Delete Task:**
```bash
# Test 9: Delete task
DELETE /api/v1/tasks/1
Authorization: Bearer <JWT_TOKEN>

Expected: 200 OK
Response:
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

#### 3. Security Tests

**Missing Token:**
```bash
# Test 10: Missing JWT token
GET /api/vapi/tasks

Expected: 401 Unauthorized
Response:
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid authorization header"
  }
}
```

**Invalid Token:**
```bash
# Test 11: Invalid JWT token
GET /api/v1/tasks
Authorization: Bearer invalid_token

Expected: 401 Unauthorized
Response:
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

**Wrong User's Task:**
```bash
# Test 12: Try to access another user's task
GET /api/v1/tasks/999
Authorization: Bearer <JWT_TOKEN>

Expected: 404 Not Found
Response:
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Task not found"
  }
}
```

#### 4. Validation Tests

**Empty Title:**
```bash
# Test 13: Create task with empty title
POST /api/v1/tasks
Authorization: Bearer <JWT_TOKEN>
Body:
{
  "title": "   ",
  "description": "Description"
}

Expected: 400 Bad Request
Response:
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "    "message": "Title is required"
  }
}
```

**Title Too Long:**
```bash
# Test 14: Create task with title > 200 chars
POST /api/v1/tasks
Authorization: Bearer <JWT_TOKEN>
Body:
{
  "title": "This title is way too long and exceeds the 200 character limit..."
}

Expected: 400 Bad Request
Response:
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title must be 200 characters or less"
  }
}
```

---

## Testing Tools

### 1. Swagger UI (FastAPI Auto-Generated)

**Access:** `http://localhost:8000/docs`

**Features:**
- Interactive API documentation
- "Try it out" functionality
- Request/response examples
- Schema definitions
- Authorization button for protected endpoints

**Usage:**
1. Open Swagger UI
2. Click endpoint to expand details
3. Click "Try it out"
4. Fill in parameters
5. Add Authorization header: `Bearer <your_jwt_token>`
6. Click "Execute"

---

### 2. Postman Collections

**Create Collection:**

**Collection: Phase 2 Todo API**
- Environment Variables:
  - `base_url`: `http://localhost:`
  - `jwt_token`: `your_jwt_token_here`

**Requests:**

**1. Health Check**
- Name: Health Check
- Method: GET
- URL: `/api/v1/health`
- No auth required

**2. User Signup**
- Name: Signup
- Method: POST
- URL: `/api/v1/auth/signup`
- Body:
  ```json
  {
    "email": "test@example.com",
    "    "password": "testPassword123",
    "    "name": "Test User"
  }
  ```

**3. User Login**
- Name: Login
- Method: POST
- URL: `/api/v1/auth/login`
- Body:
  ```json
  {
    "email": "test@example.com",
    "password": "    "testPassword123"
  }
  ```

**4. Create Task**
- Name: Create Task
- Method: POST
- URL: `/api/v1/tasks`
- Headers: Authorization: Bearer `{{jwt_token}}`
- Body:
  ```json
  {
    "title": "Test Task",
    "description": "Test Description"
  }
  ```

**5. Get Tasks**
- Name: Get All Tasks
- Method: GET
- URL: `/api/v1/tasks`
- Headers: Authorization: Bearer `{{jwt_token}}`

**6. Get Task by ID**
- Name: Get Task
- Method: GET
- URL: `/api/v1/tasks/1`
- Headers: Authorization: Bearer `{{jwt_token}}`

**7. Update Task**
- Name: Update Task
- Method: PUT
- URL: `/api/v1/tasks/1`
- Headers: Authorization: Bearer `{{jwt_token}}`
- Body:
  ```json
  {
    "title": "Updated Task Title"
  }
  ```

**8. Toggle Complete**
- Name: Toggle Complete
- Method: PATCH
- URL: `/api/v1/tasks/1/complete`
- Headers: Authorization: Bearer `{{jwt_token}}`

**9. Delete Task**
- Name: Delete Task
- Method: DELETE
- URL: `/api/v1/tasks/1`
- Headers: Authorization: Bearer `{{jwt_token}}`

**10. Get Current User**
- Name: Get Current User
- Method: GET
- URL: `/api/v1/auth/me`
- Headers: Authorization: Bearer `{{jwt_token}}`

---

### 3. Python Test Scripts

**Automated Test Suite:**
```python
# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_signup():
    """Test user signup"""
    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json={
        "email": "test@example.com",
        "password": "testPassword123",
        "name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    return data["data"]["token"]

def test_login(token):
    """Test user login"""
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "testPassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    return data["data"]["token"]

def test_create_task(token):
    """Test create task endpoint"""
    response = requests.post(
        f"{BASE_URL}/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] == True
    return data["data"]["id"]

def test_get_tasks(token):
    """Test get tasks endpoint"""
    response = requests.get(
        f"{BASE_URL}/api/v1/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["data"]["tasks"]) >= 0

def test_data_isolation():
    """Test that users can only see their own tasks"""
    # Create two users
    token1 = signup_and_get_token("user1@example.com")
    token2 = signup_and_get_token("user2@example.com")

    # Create task for user 1
    task_id = test_create_task(token1)

    # User 2 tries to access User 1's task
    response = requests.get(
        f"{BASE_URL}/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 404
    data = response.json()
    assert data["success"] == False

def test_invalid_token():
    """Test that invalid tokens are rejected"""
    response = requests.get(
        f"{BASE_URL}/api/v1/tasks",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    data = response.json()
    assert data["success"] == False
```

---

## Test Execution

### Running Tests

**Using Python:**
```bash
cd backend
python test_api.py
```

**Using pytest:**
```bash
cd backend
pytest tests/ -v
```

**Using Postman:**
1. Import collection
2. Set environment variables
3. Run collection in order
4. Verify all tests pass

---

## Test Results Documentation

### Test Report Template

**API Test Report**

**Date:** 2026-01-17

**Environment:** Development

**Backend Version:** 1.0.0

**Results:**

| Test Case | Endpoint | Status | Response Code | Result |
|----------|----------|--------|---------------|--------|
| Health Check | GET /api/v1/health | ✅ PASS | 200 | Database connected |
| User Signup | POST /api/v1/auth/signup | ✅ PASS | 201 | User created, token issued |
| User Login | POST /api/v1/auth/login | ✅ PASS | 200 | Token issued |
| Get Current User | GET /api/v1/auth/me | ✅ PASS | 200 | User info returned |
| Create Task | POST /api/v1/tasks | ✅ PASS | 201 | Task created |
| Get Tasks | GET /api/v1/tasks | ✅ PASS | 200 | Tasks returned |
| Get Task | GET /api/v1/tasks/{id} | ✅ PASS | 200 | Task details returned |
| Update Task | PUT /api/v1/tasks/{id} | ✅ PASS | 200 | Task updated |
| Toggle Complete | PATCH /api/v1/tasks/{id}/complete | ✅ PASS | 200 | Task toggled |
| Delete Task | DELETE /api/v1/tasks/{id} | ✅ PASS |  | **Task deleted** |

**Security Tests:**

| Test Case | Description | Status | Result |
|----------|-------------|--------|--------|
| 10 | Missing JWT token | ✅ PASS | 401 Unauthorized |
| 11 | Invalid JWT token | ✅ PASS | 401 Unauthorized |
| 12 | Access other user's task | ✅ PASS | 404 Not Found |

**Validation Tests:**

| Test Case | Description | Status | Result |
|----------|-------------|--------|--------|
| 13 | Empty title | ✅ PASS | 400 Validation Error |
| 14 | Title > 200 chars | ✅ PASS | 400 Validation Error |

**Summary:**
- **Total Tests:** 14
- **Passed:** 14
- **Failed:** 0
- **Pass Rate:** 100%

---

## Error Handling Tests

### Error Responses

**400 Bad Request:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required"
  }
}
```

**401 Unauthorized:**
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Missing or invalid authorization header"
  }
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "|
```
```

---

## Security Validation

### Data Isolation Tests

**Test: User Data Privacy**
1. Create User 1 and User 2
2. Login as User 1, create task with title "User 1 Task"
3. Login as User 2
4. Try to GET /api/v1/tasks/{user1_task_id}
5. **Expected:** 404 Not Found (User 2 can't see User 1's task)

### Authentication Tests

**Test: Token Expiry**
1. Login and get JWT token
2. Decode JWT to find expiry time
3. Wait or modify token to make it expired
4. Try expired token
5. **Expected:** 401 Unauthorized with "expired" error

**Test: Token Tampering**
1. Take valid JWT token
2. Modify token (change one character)
3. Send request with tampered token
4. **Expected:** 401 Unauthorized with "Invalid token" error

---

## Performance Tests

### Response Time Tests

**Target:** API responses should be < 300ms (p95)

**Tests:**
- **Signup:** Should complete in < 500ms
- **Login:** Should complete in < 500ms
- **List Tasks (100 items):** Should return < 1s
- **Create Task:** Should complete in < 200ms
- **Update Task:** Should complete in < 200ms
- **Delete Task:** Should complete in < 200ms

---

## Load Testing

### Load Test Scenarios

**Scenario 1: Concurrent Users**
```python
import asyncio
import aiohttp

async def simulate_user(user_id: int):
    async with aiohttp.ClientSession() as session:
        # Login
        async with session.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"email": f"user{user_id}@example.com", "password": "password123"}
        ) as response:
            token = response.json()["data"]["token"]

        headers = {"Authorization": f"Bearer {token}"}

        # Create 10 tasks
        for i in range(10):
            await session.post(
                f"{BASE_URL}/api/v1/tasks",
                json={"title": f"Task {i}", "description": "Description"},
                headers=headers
            )
```

**Scenario 2: Large Dataset Performance**
- Insert 1000 tasks
- Query with pagination
- Measure response times
- Verify pagination works correctly

---

## Postman Test Collection Example

**Collection Name:** "Todo App API Test Suite"

**Environment:**
- `base_url`: `http://localhost:8000/api/v1`
- `jwt_token`: `{{login.response.body.data.data.token}}`

**Tests:**

1. **Health Check**
2. **User Signup**
3. **User Login** (sets token variable)
4. **Get Current User**
5. **Create Task**
6. **List Tasks**
7. **Get Single Task**
8. **Update Task**
9. **Tests** (folder with sub-tests for each operation)

---

## Quality Checklist

Before completing testing, verify:

- [ ] All endpoints tested (POST, GET, PUT, DELETE, PATCH)
- [ ] Authentication tested (signup, login, token verification)
- [ ] Error cases tested (400, 401, 403, 404, 500)
- [ ] Data isolation verified (users can't see each other's data)
- [ ] Input validation tested (empty fields, length constraints)
- ] Performance tests passed (response times within budget)
- [ ] Swagger UI documentation is complete
- [ ] Postman collection created
- | Test cases documented
- | Security tests passed
- | Edge cases covered
- | Load testing completed

---

## Related Skills

- `fastapi-backend` - Create test cases for backend APIs
- `spec-writing` - Review specifications to create test cases
- `system-architecture` - Understand system flows for test design

---

## Usage Instructions

When invoked, this skill will:

1. **Review Specifications:** Review API specs and architecture
2. **Design Tests:** Create comprehensive test plan
3. **Create Test Suite:** Create automated test scripts
4. **Execute Tests:** Run tests and collect results
5. **Document Results:** Create test report
6. **Report:** Provide detailed test results with pass/fail rates

---

## File Locations

Test artifacts created:
- Test scripts: `backend/tests/` directory
- Postman collection: `postman_collections/` directory
- Test documentation: `backend/TEST_REPORT.md`

---

## Version History

- **v1.0** (2026-01-17): Initial skill definition

---

**Skill Status:** ✅ Active
**Phase:** Phase II - Full-Stack Web Application
