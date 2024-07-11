from fastapi.middleware.cors import CORSMiddleware
from utils import get_prompt
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from generation import gemini

# import models.gemini as gemini
# import models.vistral7b as vistral7b

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBrsEuLPKV0zkGW3GLIbxupb2ANGOdg7sg"


llm_call = {
    "gemini": gemini.generate_response,
    # "vistral-7b-chat": vistral7b.generate_response,
}

DEFAULT_MODEL = "gemini"


@app.post("/stream")
async def stream_response(request: Request):
    body = await request.json()
    message = body.get("message", "")
    model = body.get("model", DEFAULT_MODEL)
    prompt = get_prompt(message)  # add returning reference to the prompt
    print(prompt)

    if not prompt:
        return {"error": "Prompt is required"}
    # return StreamingResponse(stream_gemini_api(prompt), media_type="application/json")
    data = await llm_call[model](prompt)
    resp = {"answer": data, "source_documents": None}
    return resp


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
