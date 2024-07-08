import json

import httpx
from fastapi.middleware.cors import CORSMiddleware
from utils import get_prompt
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBrsEuLPKV0zkGW3GLIbxupb2ANGOdg7sg'



async def stream_gemini_api(prompt):
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]})
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=None) as client:
        res = await client.post(API_URL, headers=headers, data=payload)
        res = res.json()
        text = res["candidates"][0]["content"]["parts"][0]["text"]
        return {"result":text,
                "source_documents":None}
            # async for chunk in response.aiter_bytes():
            #     yield chunk


@app.post("/stream")
async def stream_response(request: Request):
    body = await request.json()
    message = body.get("message", "")
    prompt = get_prompt(message)
    print(prompt)

    if not prompt:
        return {"error": "Prompt is required"}
    # return StreamingResponse(stream_gemini_api(prompt), media_type="application/json")
    data = await stream_gemini_api(prompt)
    return data

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
