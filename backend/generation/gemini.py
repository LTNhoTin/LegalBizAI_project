import json
import httpx


async def generate_response(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBFxeqWY-1HJGl_1nnbAdtCo1CAWMjQ9Kc"

    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]})
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(url, headers=headers, data=payload)
    response_json = response.json()
    text = response_json["candidates"][0]["content"]["parts"][0]["text"]

    return text
