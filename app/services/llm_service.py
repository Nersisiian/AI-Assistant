from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def generate_response(messages):
    res = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return res.choices[0].message.content


async def stream_response(messages):
    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content