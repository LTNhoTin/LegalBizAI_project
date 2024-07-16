import requests
import json

url = "https://set-barnacle-refined.ngrok-free.app/vistral"

# url = "https://dd0b-118-69-64-142.ngrok-free.app/v1/models/vistral`"

payload = {"contents": [{"parts": [{"text": "bạn là ai"}]}]}
# payload = {"message": "bạn là ai", "model": "legalbizai-vistral"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Failed:", response.status_code, response.text)
