import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

# Paths
PDF_PATH = r"C:\Users\Bhava\OneDrive\Desktop\HR_Chatbot\HR-Policy.pdf"
INDEX_PATH = "data/hr_index.faiss"
META_PATH = "data/hr_meta.pkl"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def build_index():
    text = load_pdf(PDF_PATH)
    chunks = chunk_text(text)

    embeddings = model.encode(chunks, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index + metadata
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"✅ Index built with {len(chunks)} chunks.")

if __name__ == "__main__":
    build_index()
