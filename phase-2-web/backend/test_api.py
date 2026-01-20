"""
Test Backend API Endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_backend():
    print("=== Backend API Testing ===\n")

    # 1. Health Check
    print("1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

    # 2. Signup
    print("2. Testing Signup...")
    signup_data = {
        "email": "test2@example.com",
        "password": "testPassword123",
        "name": "Test User 2"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")

    if result.get("success"):
        token = result["data"]["token"]
        print(f"Token: {token[:50]}...\n")

        # 3. Login
        print("3. Testing Login...")
        login_data = {
            "email": "test2@example.com",
            "password": "testPassword123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}\n")

        if result.get("success"):
            token = result["data"]["token"]
            headers = {"Authorization": f"Bearer {token}"}

            # 4. Get Current User
            print("4. Testing Get Current User...")
            response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}\n")

            # 5. Create Task
            print("5. Testing Create Task...")
            task_data = {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
            response = requests.post(f"{BASE_URL}/api/v1/tasks", json=task_data, headers=headers)
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}\n")

            # 6. List Tasks
            print("6. Testing List Tasks...")
            response = requests.get(f"{BASE_URL}/api/v1/tasks", headers=headers)
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}\n")

            if result.get("success") and len(result["data"]["tasks"]) > 0:
                task_id = result["data"]["tasks"][0]["id"]
                print(f"Got task ID: {task_id}\n")

                # 7. Get Single Task
                print(f"7. Testing Get Task {task_id}...")
                response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}", headers=headers)
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}\n")

                # 8. Update Task
                print(f"8. Testing Update Task {task_id}...")
                update_data = {"title": "Buy groceries and fruits"}
                response = requests.put(f"{BASE_URL}/api/v1/tasks/{task_id}", json=update_data, headers=headers)
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}\n")

                # 9. Toggle Complete
                print(f"9. Testing Toggle Complete {task_id}...")
                response = requests.patch(f"{BASE_URL}/api/v1/tasks/{task_id}/complete", headers=headers)
                print(f"Status: {response.status_code}")
                print(f"Response: {json.dumps(response.json(), indent=2)}\n")

                # 10. Delete Task (commented out to keep the task)
                # print(f"10. Testing Delete Task {task_id}...")
                # response = requests.delete(f"{BASE_URL}/api/v1/tasks/{task_id}", headers=headers)
                # print(f"Status: {response.status_code}")
                # print(f"Response: {json.dumps(response.json(), indent=2)}\n")

    print("=== All Tests Complete ===")

if __name__ == "__main__":
    test_backend()
