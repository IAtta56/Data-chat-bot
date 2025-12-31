import requests
import sys
import time

def check_service(url, name):
    print(f"Checking {name} at {url}...")
    try:
        response = requests.get(url, timeout=2)
        print(f"✅ {name} is UP. Status Code: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"XXX {name} is DOWN (Connection Refused)")
        return False
    except Exception as e:
        print(f"XXX {name} Error: {e}")
        return False

def main():
    print("Waiting 5s for services to stabilize...")
    time.sleep(5)
    
    backend_ok = check_service("http://127.0.0.1:8000/", "Backend")
    frontend_ok = check_service("http://127.0.0.1:5173/register", "Frontend Register Page")
    frontend_root = check_service("http://127.0.0.1:5173/", "Frontend Root")

    if not backend_ok or not frontend_root:
        print("One or more critical services are down.")
        sys.exit(1)
    
    print("All critical services reachable.")

if __name__ == "__main__":
    main()
