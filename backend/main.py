import json
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from utils import get_prompt

app = FastAPI()

API_URL_LEGALBIZAI = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBFxeqWY-1HJGl_1nnbAdtCo1CAWMjQ9Kc"

async def stream_gemini_api(prompt):
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]})
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", API_URL_LEGALBIZAI, headers=headers, data=payload) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

async def get_response_from_gpt(prompt):
    payload = {
        "prompt": prompt,
        "max_tokens": 100
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer YOUR_OPENAI_API_KEY"
    }
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(API_URL_GPT, headers=headers, json=payload)
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("text", "")

@app.post("/stream")
async def stream_response(request: Request):
    body = await request.json()
    message = body.get("message", "")
    model = body.get("model", "LegalbizAI")
    prompt = get_prompt(message)
    print(prompt)

    if not prompt:
        return JSONResponse(content={"error": "Prompt is required"}, status_code=400)

    if model == "LegalbizAI_gpt":
        result = await get_response_from_gpt(prompt)
        return JSONResponse(content={"result": result})
    else:
        return StreamingResponse(stream_gemini_api(prompt), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
