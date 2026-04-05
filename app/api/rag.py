from fastapi import APIRouter, UploadFile, File
import os

from app.utils.pdf_loader import extract_text_from_pdf
from app.utils.text_splitter import split_text
from app.services.rag_service import add_documents

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(path)
    chunks = split_text(text)

    add_documents(chunks)

    return {"message": "PDF processed"}