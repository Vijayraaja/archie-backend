import requests

url = 'http://127.0.0.1:5000/add_row'
data = {"row": ["10000", "Pinheiro Apartment", "May 2025"]}

response = requests.post(url, json=data)
print(response.json())
