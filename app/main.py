from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_assistant"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

app = FastAPI(title="AI Assistant API", version="1.0")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class UserCreate(BaseModel):
    name: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "AI Assistant is running!"}

@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate):
    async with async_session() as session:
        db_user = User(name=user.name, email=user.email)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

@app.post("/auth/login")
async def login(email: str):
    async with async_session() as session:
        result = await session.execute(
            "SELECT * FROM users WHERE email=:email", {"email": email}
        )
        user = result.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": f"Logged in as {email}"}

@app.post("/chat")
async def chat(message: str):
    # временно просто эхо
    return {"response": f"You said: {message}"}

@app.get("/memory")
async def memory():
    
    return {"memory": []}

# --- /rag пример ---
@app.post("/rag")
async def rag(query: str):
    # временно заглушка
    return {"answer": f"RAG simulated answer to: {query}"}