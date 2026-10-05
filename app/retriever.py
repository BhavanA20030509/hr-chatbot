```python
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache
import numpy as np
import os


# ============================================================
# 1. Find the project folder automatically
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# HR-Policy.pdf is located in the root of the project
PDF_PATH = os.path.join(BASE_DIR, "HR-Policy.pdf")


# ============================================================
# 2. Load the HR Policy PDF
# ============================================================

loader = PyPDFLoader(PDF_PATH)
documents = loader.load()


# ============================================================
# 3. Split PDF into smaller chunks
# ============================================================

text_splitter = CharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)


# ============================================================
# 4. Create HuggingFace embeddings
# ============================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# 5. Create FAISS vector database
# ============================================================

db = FAISS.from_documents(
    docs,
    embeddings
)


# ============================================================
# 6. Search HR Policy
# ============================================================

def search(query: str):
    """Search HR policy document and return the most relevant results."""

    # Step 1: Retrieve initial candidates
    candidates = db.similarity_search(
        query,
        k=8
    )

    if not candidates:
        return {
            "answer": "Sorry, I couldn't find relevant information.",
            "sources": []
        }


    # ========================================================
    # Step 2: Re-rank results using cosine similarity
    # ========================================================

    query_vec = embeddings.embed_query(query)

    scored = []

    for res in candidates:

        doc_vec = embeddings.embed_query(
            res.page_content
        )

        score = np.dot(query_vec, doc_vec) / (
            np.linalg.norm(query_vec) *
            np.linalg.norm(doc_vec)
        )

        scored.append(
            (res, score)
        )


    # Sort from highest similarity to lowest
    scored = sorted(
        scored,
        key=lambda x: x[1],
        reverse=True
    )


    # Select top 3 results
    results = [
        r for r, _ in scored[:3]
    ]


    # ========================================================
    # Step 3: Clean and remove duplicate text
    # ========================================================

    seen = set()
    answer_parts = []

    for res in results:

        text = res.page_content.replace(
            "\n",
            " "
        ).strip()

        if text not in seen:

            answer_parts.append(text)
            seen.add(text)


    # Combine the retrieved chunks
    answer = " ".join(answer_parts)


    # ========================================================
    # Step 4: Collect source information
    # ========================================================

    sources = []

    for res in results:

        src = {
            "title": res.metadata.get(
                "title",
                "HR-Policy"
            ),

            "page": res.metadata.get(
                "page",
                "?"
            ),

            "source": res.metadata.get(
                "source",
                ""
            )
        }

        if src not in sources:
            sources.append(src)


    # ========================================================
    # Step 5: Return final response
    # ========================================================

    return {
        "answer": answer,
        "sources": sources
    }


# ============================================================
# 7. Cache repeated questions
# ============================================================

@lru_cache(maxsize=100)
def cached_search(query: str):
    """Cache repeated searches to improve response speed."""

    return search(query)
```
