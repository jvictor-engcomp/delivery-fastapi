import requests

header = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMSIsImV4cCI6MTc3MjYzNTM2OX0.fZasE0c9M65k8YBAtUZr4xbd2OOgnE7m8LMUmpHQvr8'
}

request = requests.get(url= 'http://127.0.0.1:8000/auth/refresh', headers= header)
print(request.json())