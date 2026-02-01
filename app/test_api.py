import requests
import json

BASE_URL = "http://localhost:8000"

def test_input_moderation():
    url = f"{BASE_URL}/moderate/input"
    
    test_cases = [
        {"user_input": "Hello, how can I help you today?"},
        {"user_input": "You are stupid and worthless!"},
        {"user_input": "What's the weather like?"}
    ]
    
    print("=" * 50)
    print("INPUT MODERATION TESTS")
    print("=" * 50)
    
    for case in test_cases:
        print(f"\nInput: {case['user_input']}")
        response = requests.post(url, json=case)
        result = response.json()
        print(f"Overall Passed: {result['overall_passed']}")
        for metric_result in result['results']:
            print(f"  - {metric_result['metric_name']}: {metric_result['score']:.2f} ({'PASS' if metric_result['passed'] else 'FAIL'})")
            if metric_result['reason']:
                print(f"    Reason: {metric_result['reason']}")

def test_output_moderation():
    url = f"{BASE_URL}/moderate/output"
    
    test_cases = [
        {"ai_response": "I'm happy to help you with that!"},
        {"ai_response": "That's a terrible idea and you should be ashamed."},
        {"ai_response": "Based on the data, here are the results."}
    ]
    
    print("\n" + "=" * 50)
    print("OUTPUT MODERATION TESTS")
    print("=" * 50)
    
    for case in test_cases:
        print(f"\nOutput: {case['ai_response']}")
        response = requests.post(url, json=case)
        result = response.json()
        print(f"Overall Passed: {result['overall_passed']}")
        for metric_result in result['results']:
            print(f"  - {metric_result['metric_name']}: {metric_result['score']:.2f} ({'PASS' if metric_result['passed'] else 'FAIL'})")
            if metric_result['reason']:
                print(f"    Reason: {metric_result['reason']}")

if __name__ == "__main__":
    print("Testing Content Moderation API...")
    print("Make sure the API is running on http://localhost:8000\n")
    
    try:
        test_input_moderation()
        test_output_moderation()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API. Make sure it's running with: python main.py")
    except Exception as e:
        print(f"\nError: {str(e)}")
