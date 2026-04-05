# 🚀 AI Assistant API (Mini ChatGPT)

Production-ready AI Assistant API built with FastAPI, featuring memory, RAG (documents), authentication, and streaming responses.

---

## ✨ Features

* 💬 Chat with AI (OpenAI)
* ⚡ Streaming responses (like ChatGPT)
* 🧠 Memory (conversation history)
* 📚 RAG (PDF document support)
* 🔐 JWT Authentication
* 🗄 PostgreSQL database
* 🐳 Docker support

---

## 🏗 Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy (async)
* OpenAI API
* FAISS (vector search)
* Docker

---

## 📦 Installation

### 1. Clone repo

```bash
git clone https://github.com/your-username/ai-assistant.git
cd ai-assistant
```

### 2. Setup environment

```bash
cp .env.example .env
```

Fill in:

```
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/ai_db
SECRET_KEY=your_secret
OPENAI_API_KEY=your_key
```

---

## ▶️ Run with Docker

```bash
docker-compose up --build
```

---

## 🔐 Auth

### Register

POST /auth/register

### Login

POST /auth/login

---

## 💬 Chat

### Normal

POST /chat

### Streaming

POST /chat/stream

---

## 📚 RAG (Documents)

### Upload PDF

POST /rag/upload

---

## 🧠 Architecture

User → API → Memory → RAG → LLM → Response

---

## 🚀 Future Improvements

* Real embeddings (OpenAI)
* Redis caching
* Tools (calculator, search)
* Frontend UI

---

## 👨‍💻 Author

Nersisiian
