from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache
import numpy as np
import os

PDF_PATH = r"C:\Users\Bhava\OneDrive\Desktop\HR_Chatbot\HR-Policy.pdf"

# Load full PDF
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

# Split into chunks
text_splitter = CharacterTextSplitter(chunk_size=1200, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Build FAISS index
db = FAISS.from_documents(docs, embeddings)

def search(query: str):
    """Search HR policy document for answers with re-ranking."""
    # Step 1: Initial retrieval
    candidates = db.similarity_search(query, k=8)  # get more candidates first
    if not candidates:
        return {"answer": "Sorry, I couldn’t find relevant info.", "sources": []}

    # Step 2: Re-rank with cosine similarity
    query_vec = embeddings.embed_query(query)
    scored = []
    for res in candidates:
        doc_vec = embeddings.embed_query(res.page_content)
        score = np.dot(query_vec, doc_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(doc_vec))
        scored.append((res, score))

    # Sort by cosine score, pick top 3
    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    results = [r for r, _ in scored[:3]]

    # Step 3: Clean and deduplicate text
    seen = set()
    answer_parts = []
    for res in results:
        text = res.page_content.replace("\n", " ").strip()
        if text not in seen:
            answer_parts.append(text)
            seen.add(text)

    # Merge into single response
    answer = " ".join(answer_parts)

    # Collect unique sources
    sources = []
    for res in results:
        src = {
            "title": res.metadata.get("title", "HR-Policy"),
            "page": res.metadata.get("page", "?"),
            "source": res.metadata.get("source", "")
        }
        if src not in sources:
            sources.append(src)

    return {"answer": answer, "sources": sources}

# ✅ Caching layer
@lru_cache(maxsize=100)
def cached_search(query: str):
    """Cache wrapper around search() to speed up repeated queries."""
    return search(query)
