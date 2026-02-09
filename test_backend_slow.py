#!/usr/bin/env python3
"""
Backend Test with Extended Timeout (for cold starts)
"""

import requests
import json
import time

BACKEND_URL = "https://customer-service-ai-system.onrender.com"

print("=" * 70)
print("TESTING BACKEND WITH COLD START SUPPORT")
print("=" * 70)
print(f"Backend: {BACKEND_URL}")
print("\n⚠️  This may take 30-60 seconds on first request (cold start)...")
print("Please be patient!\n")

try:
    start = time.time()

    response = requests.post(
        f"{BACKEND_URL}/api/query",
        json={
            "question": "How to get a loan?",
            "user_name": "Test User"
        },
        timeout=90  # 90 second timeout for cold start
    )

    duration = time.time() - start

    print(f"✓ Response received in {duration:.1f} seconds")
    print(f"HTTP Status: {response.status_code}\n")

    if response.status_code == 200:
        result = response.json()

        if result.get('success'):
            print("✅ SUCCESS! Backend is working!\n")
            print("=" * 70)
            print("Response:")
            print("=" * 70)
            print(f"Original Question: {result['original_question']}")
            print(f"Reformulated Query: {result['reformulated_query']}")
            print(f"Answer: {result['answer'][:100]}...")
            print(f"Confidence: {result['confidence_score']}%")
            print(f"Response Time: {result['response_time_ms']}ms")
            print("=" * 70)
            print("\n✅ YOUR BACKEND IS FULLY FUNCTIONAL!")
            print("The frontend should now work. Try refreshing and testing again.")
        else:
            print("❌ Backend returned error:")
            print(json.dumps(result, indent=2))
            print("\n→ Check Render logs for details")
    else:
        print(f"❌ HTTP Error {response.status_code}")
        print(response.text)
        print("\n→ Check Render logs for details")

except requests.exceptions.Timeout:
    print("❌ Request timed out after 90 seconds")
    print("\nPossible issues:")
    print("  1. ANTHROPIC_API_KEY not set in Render environment variables")
    print("  2. Vector database not initialized (init_rag.py failed)")
    print("  3. Backend crashed on API call")
    print("\n→ Check Render logs for error messages")

except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend")
    print("  → Backend service might be down")
    print("  → Check Render dashboard service status")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
