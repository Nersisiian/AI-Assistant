from sqlalchemy.future import select
from app.db.models import User
from app.core.security import hash_password, verify_password

async def create_user(db, email, password):
    user = User(email=email, password=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db, email, password):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password):
        return None

    return user