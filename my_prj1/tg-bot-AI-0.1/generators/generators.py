import asyncio
from mistralai import Mistral
import os
from dotenv import load_dotenv
load_dotenv()
async def generate(content):
    async with Mistral(
        api_key=os.getenv("AI_TOKEN"),
    ) as mistral:
        res = await mistral.chat.complete_async(model="mistral-large-latest", messages=[
            {
                "content": content,
                "role": "user",
            },
        ])
        if res is not None:
            return res
