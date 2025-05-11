import requests

url = 'https://archie-bridge.onrender.com/create_sheet'
data = { "title": "TestSheet" }

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Raw text:", response.text)  # ← this will reveal the actual error message
