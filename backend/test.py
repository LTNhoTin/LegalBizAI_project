import asyncio
import httpx
from utils import get_prompt


async def stream_post_message(message: str):
    url = "http://localhost:8000/stream"
    payload = {"message": message}
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, headers=headers, json=payload) as response:
            async for chunk in response.aiter_text():
                print(chunk, end="")


async def main():
    while True:
        message = input("Enter your message: ")
        if message.lower() in {"exit", "quit"}:
            break
        await stream_post_message(message)


if __name__ == "__main__":
    asyncio.run(main())
