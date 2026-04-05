from sqlalchemy.future import select
from app.db.models import Message

async def get_history(db, user_id):
    result = await db.execute(
        select(Message).where(Message.user_id == user_id)
    )
    messages = result.scalars().all()

    return [{"role": m.role, "content": m.content} for m in messages]


async def save_message(db, user_id, role, content):
    msg = Message(user_id=user_id, role=role, content=content)
    db.add(msg)
    await db.commit()