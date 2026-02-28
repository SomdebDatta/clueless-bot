import requests
from datetime import date

payload = {
        "categoryId": 0,
        "word": "dummy",
        "challengeDate": date.today().isoformat()
    }
response = requests.post(url="https://api.lessgames.com/clueless/guess", json=payload)
print(response)
print(response.status_code)
# print(response.json())