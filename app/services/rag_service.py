import faiss
import numpy as np
from app.utils.embeddings import fake_embedding

index = faiss.IndexFlatL2(768)
documents = []

def add_documents(chunks):
    vectors = []

    for chunk in chunks:
        emb = fake_embedding(chunk)
        vectors.append(emb)
        documents.append(chunk)

    index.add(np.array(vectors).astype("float32"))

def search(query, k=3):
    emb = fake_embedding(query)
    D, I = index.search(np.array([emb]).astype("float32"), k)
    return [documents[i] for i in I[0] if i < len(documents)]