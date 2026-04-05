from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import ChatRequest
from app.services.memory_service import get_history, save_message
from app.services.rag_service import search
from app.services.llm_service import generate_response, stream_response
from app.utils.deps import get_current_user, get_db

router = APIRouter()

@router.post("/")
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    history = await get_history(db, user.id)
    docs = search(req.message)

    messages = [{"role": "system", "content": "\n".join(docs)}] + history + [
        {"role": "user", "content": req.message}
    ]

    answer = await generate_response(messages)

    await save_message(db, user.id, "user", req.message)
    await save_message(db, user.id, "assistant", answer)

    return {"response": answer}


@router.post("/stream")
async def chat_stream(req: ChatRequest, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    history = await get_history(db, user.id)
    docs = search(req.message)

    messages = [{"role": "system", "content": "\n".join(docs)}] + history + [
        {"role": "user", "content": req.message}
    ]

    async def generator():
        full = ""
        async for chunk in stream_response(messages):
            full += chunk
            yield chunk

        await save_message(db, user.id, "user", req.message)
        await save_message(db, user.id, "assistant", full)

    return StreamingResponse(generator(), media_type="text/plain")