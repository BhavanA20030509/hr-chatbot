from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import retriever   # 👈 FIXED relative import

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    question: str

# Routes
@app.post("/query")
def answer_question(request: QueryRequest):
    result = retriever.search(request.question)
    return {"answer": result["answer"], "sources": result["sources"]}

@app.get("/")
def read_root():
    return {"message": "HR Chatbot API is running!"}
