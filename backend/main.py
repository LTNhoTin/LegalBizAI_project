import json
import httpx
from fastapi.middleware.cors import CORSMiddleware
from utils import RetrieveContent
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
    allow_methods=["*"],
    allow_headers=["*"],
)



async def stream_get_answer(model, prompt):
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]})
    headers = {"Content-Type": "application/json"}
    
    if model == "LegalBizAI":
        API_URL = 'xxx'

    elif model == "LegalBizAI_pro":
        API_URL = 'xxx'

    async with httpx.AsyncClient(timeout=None) as client:
        res = await client.post(API_URL, headers=headers, data=payload)
        res = res.json()
        text = res["candidates"][0]["content"]["parts"][0]["text"]
        return text

            # async for chunk in response.aiter_bytes():
            #     yield chunk

    # return = {
    #     "candidates":[{"content":{"parts":[{"text": Vistral7b_return}]}}]
    # }

@app.post("/stream")
async def stream_response(request: Request):
    body = await request.json()
    message = body.get("message", "")
    model = body.get("model", "")
    print(message)
    print(model)
    retrieve_content =  RetrieveContent(message)
    prompt = retrieve_content.get_prompt()
    # print(prompt)
    if not prompt:
        return {"error": "Prompt is required"}
    # return StreamingResponse(stream_gemini_api(prompt), media_type="application/json")
    answer = await stream_get_answer(model, prompt)

    referenced_response =  retrieve_content.get_true_references(answer)
    print(referenced_response)
    return referenced_response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
