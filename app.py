import requests

print("🐳 Live editing works! No rebuild needed! 🚀")
try:
    response = requests.get("https://httpbin.org/json")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"API Response: {response.json()}")
    else:
        print(f"API Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")