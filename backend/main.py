import json

import httpx

from app.backend.utils import get_prompt
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBFxeqWY-1HJGl_1nnbAdtCo1CAWMjQ9Kc"


async def stream_gemini_api(prompt):
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]})
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", API_URL, headers=headers, data=payload) as response:
            async for chunk in response.aiter_bytes():
                yield chunk


@app.post("/stream")
async def stream_response(request: Request):
    body = await request.json()
    message = body.get("message", "")
    prompt = get_prompt(message)
    print(prompt)

    if not prompt:
        return {"error": "Prompt is required"}
    return StreamingResponse(stream_gemini_api(prompt), media_type="application/json")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
