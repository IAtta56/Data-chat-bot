import requests

url = "http://127.0.0.1:8000/auth/register"
payload = {"email": "test@example.com", "password": "test123"}
response = requests.post(url, json=payload)
print("Status:", response.status_code)
print("Response:", response.text)
