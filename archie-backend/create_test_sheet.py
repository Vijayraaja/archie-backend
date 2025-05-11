import requests

url = 'https://ed1a-2001-4490-4821-ab37-4869-f893-7b6b-caa1.ngrok-free.app/create_sheet'
data = { "title": "Properties" }

response = requests.post(url, json=data)
print(response.json())
