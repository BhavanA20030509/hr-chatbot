import requests

url = "http://127.0.0.1:8000/query"
payload = {"question": "What is the leave policy?"}

response = requests.post(url, json=payload)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
