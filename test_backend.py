#!/usr/bin/env python3
"""
Backend Diagnostic Test
Tests if your Render backend is working correctly
"""

import requests
import sys
import json

# CHANGE THIS TO YOUR ACTUAL RENDER URL
BACKEND_URL = "https://customer-service-ai-system.onrender.com"

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def test_endpoint(name, url, method="GET", data=None):
    print(f"\n{name}")
    print(f"URL: {url}")
    print(f"Testing...", end="", flush=True)

    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=data, timeout=30)

        print(f" ✓ Connected (HTTP {response.status_code})")

        if response.status_code == 200:
            print("Response:")
            try:
                print(json.dumps(response.json(), indent=2))
                return True
            except:
                print(response.text[:200])
                return True
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(response.text[:200])
            return False

    except requests.exceptions.ConnectionError:
        print(" ❌ FAILED - Cannot connect to backend")
        print("   → Backend might not be deployed or URL is wrong")
        return False
    except requests.exceptions.Timeout:
        print(" ❌ FAILED - Request timed out")
        print("   → Backend is too slow or not responding")
        return False
    except Exception as e:
        print(f" ❌ FAILED - {str(e)}")
        return False

def main():
    print_section("BACKEND DIAGNOSTIC TEST")
    print(f"Testing backend: {BACKEND_URL}")

    results = []

    # Test 1: Health Check
    print_section("Test 1: Health Check")
    results.append(test_endpoint(
        "Health Endpoint",
        f"{BACKEND_URL}/health"
    ))

    # Test 2: Root Endpoint
    print_section("Test 2: Root Endpoint")
    results.append(test_endpoint(
        "Root Endpoint",
        f"{BACKEND_URL}/"
    ))

    # Test 3: Query Endpoint
    print_section("Test 3: Query Endpoint (Full Test)")
    print("⚠️  This test takes 5-10 seconds (or 30-60s on first request after cold start)")
    results.append(test_endpoint(
        "Query API",
        f"{BACKEND_URL}/api/query",
        method="POST",
        data={
            "question": "How to get a loan?",
            "user_name": "Test User"
        }
    ))

    # Summary
    print_section("DIAGNOSTIC SUMMARY")
    passed = sum(results)
    total = len(results)

    print(f"\nTests Passed: {passed}/{total}")

    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        print("Your backend is working correctly.")
        print("If frontend still doesn't work, check:")
        print("  1. Frontend URL configuration in app.js")
        print("  2. Browser console for CORS errors")
        print("  3. Make sure frontend is deployed/updated")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("\nTroubleshooting steps:")
        print("  1. Check Render dashboard - is service 'Live' (green)?")
        print("  2. Go to Render → Your Service → Logs")
        print("  3. Look for error messages in the logs")
        print("  4. Verify ANTHROPIC_API_KEY is set in Environment variables")
        print("  5. Check if BACKEND_URL in this script is correct")
        print(f"\n     Current URL: {BACKEND_URL}")
        print("\nFor detailed troubleshooting, see TROUBLESHOOTING.md")

    print("\n" + "=" * 60 + "\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
