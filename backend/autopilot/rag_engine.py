import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
docs = []

def load_and_ingest(folder="data"):
    global docs, index
    docs = []
    index = faiss.IndexFlatL2(384)

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                text = f.read()
                chunks = text.split("\n\n")  # simple chunking
                embeddings = model.encode(chunks)
                index.add(np.array(embeddings).astype("float32"))
                docs.extend(chunks)
    print(f"Ingested {len(docs)} chunks from text files.")

def search(query, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec).astype("float32"), top_k)
    return [docs[i] for i in I[0]]
