#!/bin/bash

# Test script for the Local Portal API
# This script demonstrates all CRUD operations

echo "=== Local Portal API Test Script ==="
echo

# Base URL for our API
BASE_URL="http://127.0.0.1:8000"

echo "1. Testing API root endpoint..."
curl -s "$BASE_URL/" | jq .
echo

echo "2. Creating a test user..."
RESPONSE=$(curl -s -X POST "$BASE_URL/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "demouser",
        "password": "securepassword123",
        "roles": "user,demo_access"
    }')
echo $RESPONSE | jq .
USER_ID=$(echo $RESPONSE | jq -r .id)
echo

echo "3. Getting all users..."
curl -s "$BASE_URL/users/" | jq .
echo

echo "4. Getting specific user by ID ($USER_ID)..."
curl -s "$BASE_URL/users/$USER_ID" | jq .
echo

echo "5. Updating user roles..."
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
    -H "Content-Type: application/json" \
    -d '{
        "roles": "admin,demo_access,special_privileges"
    }' | jq .
echo

echo "6. Testing duplicate username validation..."
curl -s -X POST "$BASE_URL/users/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "demouser",
        "password": "anotherpassword",
        "roles": "user"
    }' | jq .
echo

echo "7. Testing pagination (limit=1)..."
curl -s "$BASE_URL/users/?limit=1&offset=0" | jq .
echo

echo "8. Testing error handling (non-existent user)..."
curl -s "$BASE_URL/users/999" | jq .
echo

echo "9. Cleaning up - deleting test user..."
curl -s -X DELETE "$BASE_URL/users/$USER_ID"
echo "User deleted (status: 204 No Content)"
echo

echo "10. Verifying deletion..."
curl -s "$BASE_URL/users/" | jq .
echo

echo "=== All tests completed! ==="
