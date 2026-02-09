#!/bin/bash

# Backend URL - CHANGE THIS TO YOUR ACTUAL RENDER URL
BACKEND_URL="https://customer-service-ai-system.onrender.com"

echo "=========================================="
echo "BACKEND DIAGNOSTIC TEST"
echo "=========================================="
echo "Testing: $BACKEND_URL"
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
echo "URL: $BACKEND_URL/health"
echo "Expected: {\"status\":\"healthy\"}"
echo "Response:"
curl -s "$BACKEND_URL/health" || echo "❌ FAILED - Cannot reach backend"
echo -e "\n"

# Test 2: Root Endpoint
echo "Test 2: Root Endpoint"
echo "URL: $BACKEND_URL/"
echo "Expected: {\"message\":\"Customer Service Support System API\",\"status\":\"running\"}"
echo "Response:"
curl -s "$BACKEND_URL/" || echo "❌ FAILED - Cannot reach backend"
echo -e "\n"

# Test 3: Query Endpoint
echo "Test 3: Query Endpoint (this will take 5-10 seconds)"
echo "URL: $BACKEND_URL/api/query"
echo "Response:"
curl -s -X POST "$BACKEND_URL/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How to get a loan?",
    "user_name": "Test User"
  }' || echo "❌ FAILED - Cannot reach backend"
echo -e "\n"

echo "=========================================="
echo "DIAGNOSTIC COMPLETE"
echo "=========================================="
echo ""
echo "If all tests show JSON responses, your backend is working!"
echo "If you see '❌ FAILED', check:"
echo "  1. Is your Render service 'Live' (green)?"
echo "  2. Is the BACKEND_URL correct?"
echo "  3. Check Render logs for errors"
echo ""
