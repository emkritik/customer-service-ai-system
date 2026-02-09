import time
import requests
import statistics
import sys

# Change this to your production URL or keep for local
API_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"

def test_response_time():
    """Test response time with sample queries"""
    
    questions = [
        "Customer is yelling that money was stolen from his card",
        "What's the fee if account goes below minimum balance?",
        "Customer can't log into mobile app",
        "How long does mortgage approval take?",
        "How do I dispute a charge on my credit card?"
    ]
    
    times = []
    
    print(f"\nTesting API: {API_URL}")
    print("=" * 70)
    
    for i, question in enumerate(questions, 1):
        print(f"\nTest {i}/5: {question[:50]}...")
        
        start = time.time()
        
        try:
            response = requests.post(
                f"{API_URL}/api/query",
                json={
                    "question": question,
                    "user_name": "performance_test"
                },
                timeout=30
            )
            
            duration = time.time() - start
            times.append(duration)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Success in {duration:.2f}s")
                print(f"  ✓ Confidence: {result['confidence_score']}%")
                print(f"  ✓ Answer: {result['answer'][:60]}...")
            else:
                print(f"  ✗ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    if times:
        print("\n" + "=" * 70)
        print("PERFORMANCE SUMMARY")
        print("=" * 70)
        print(f"Tests completed: {len(times)}/5")
        print(f"Average time: {statistics.mean(times):.2f}s")
        print(f"Fastest: {min(times):.2f}s")
        print(f"Slowest: {max(times):.2f}s")
        print(f"Median: {statistics.median(times):.2f}s")
        print("=" * 70)
        
        if statistics.mean(times) < 10:
            print("✓ PASSED - Under 10 seconds average")
        else:
            print("✗ NEEDS IMPROVEMENT - Over 10 seconds average")
    else:
        print("\n✗ All tests failed")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CUSTOMER SERVICE SYSTEM - PERFORMANCE TEST")
    print("=" * 70)
    test_response_time()
