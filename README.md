# 🤖 HR Chatbot — AI-Powered Resume & HR Document Assistant

An AI-powered HR chatbot that allows users to upload HR-related PDF documents and ask questions about their content using **Retrieval-Augmented Generation (RAG)**.

The application processes documents, splits them into meaningful chunks, generates semantic embeddings, stores them in a **FAISS vector database**, retrieves the most relevant information for a user query, and generates an accurate response using an LLM.

## 🚀 Features

* 📄 Upload and process HR-related PDF documents
* 🔎 Semantic document search using vector embeddings
* 🧠 Retrieval-Augmented Generation (RAG)
* 🗃️ FAISS-based vector database
* 🔗 LangChain integration
* 🤖 LLM-powered question answering
* 🎯 Re-ranking of retrieved documents for better relevance
* ⚡ FastAPI backend for REST APIs
* 🖥️ Streamlit frontend for an interactive chat interface
* 📚 Supports questions based on uploaded documents
* 🔐 Modular backend architecture for future authentication and deployment

## 🏗️ Architecture

```text
                ┌─────────────────────┐
                │   User / Recruiter  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Streamlit Frontend │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   FastAPI Backend   │
                └──────────┬──────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
     ┌─────────────────┐         ┌─────────────────┐
     │ PDF Processing  │         │ User Question   │
     │ & Text Chunking │         │   Processing    │
     └────────┬────────┘         └────────┬────────┘
              │                           │
              ▼                           ▼
     ┌─────────────────┐         ┌─────────────────┐
     │ Sentence        │         │ Query Embedding │
     │ Transformer     │         └────────┬────────┘
     │ Embeddings      │                  │
     └────────┬────────┘                  │
              │                           │
              └────────────┬──────────────┘
                           ▼
                  ┌─────────────────┐
                  │      FAISS      │
                  │ Vector Database │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Retrieval &     │
                  │ Re-ranking      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │      LLM        │
                  │ Response        │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Chatbot Answer  │
                  └─────────────────┘
```

## 🔄 How It Works

### 1. Upload PDF

The user uploads an HR document such as:

* Employee policies
* HR guidelines
* Company rules
* Recruitment documents
* Leave policies
* Benefits information

### 2. Extract Text

The application extracts text from the uploaded PDF using PDF processing libraries such as **PyPDFLoader** and/or **pdfplumber**.

### 3. Text Chunking

Large documents are divided into smaller chunks so that relevant sections can be retrieved efficiently.

```text
Large PDF
   ↓
Extracted Text
   ↓
Text Chunks
   ↓
Embeddings
```

### 4. Generate Embeddings

Each text chunk is converted into a numerical vector using a **Sentence Transformer** model such as:

```text
all-MiniLM-L6-v2
```

These embeddings capture the semantic meaning of the text.

### 5. Store in FAISS

The generated embeddings are stored in a **FAISS vector index**, allowing efficient similarity search.

### 6. Ask a Question

The user can ask questions such as:

```text
What is the company's leave policy?

How many days of paid leave are employees entitled to?

What is the notice period?

What are the eligibility requirements for maternity leave?
```

### 7. Retrieve Relevant Information

The chatbot searches the FAISS index and retrieves the document chunks that are most relevant to the user's question.

### 8. Re-ranking

The retrieved results are re-ranked so that the most relevant context is passed to the language model.

### 9. Generate the Answer

The relevant document context and user question are passed to the LLM.

The chatbot then generates an answer based on the retrieved information.

## 🛠️ Tech Stack

| Technology            | Purpose                              |
| --------------------- | ------------------------------------ |
| Python                | Core programming language            |
| FastAPI               | Backend REST API                     |
| Streamlit             | Frontend / chatbot interface         |
| LangChain             | LLM and RAG pipeline                 |
| FAISS                 | Vector similarity search             |
| Sentence Transformers | Text embeddings                      |
| PyPDFLoader           | PDF document loading                 |
| pdfplumber            | PDF text extraction                  |
| LLM                   | Natural language response generation |

## 📂 Project Structure

```text
hr-chatbot/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── utils/
│
├── frontend/
│   └── app.py
│
├── data/
│   └── documents/
│
├── vectorstore/
│   └── faiss_index/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> Adjust the folder names above to match the final structure of your repository.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/BhavanA20030509/hr-chatbot.git
cd hr-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
venv\Scripts\activate
```

**Windows CMD:**

```cmd
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

Add any additional environment variables required by the LLM or backend configuration.

> Never commit API keys or other secrets to GitHub.

## ▶️ Running the Project

### Start FastAPI Backend

From the backend/project directory:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit Frontend

```bash
streamlit run app.py
```

The Streamlit interface will then open in your browser.

## 🧪 Example Workflow

```text
Upload HR Policy PDF
        ↓
Extract PDF Text
        ↓
Split Text into Chunks
        ↓
Generate Embeddings
        ↓
Store Embeddings in FAISS
        ↓
User Asks Question
        ↓
Retrieve Relevant Chunks
        ↓
Re-rank Results
        ↓
Send Context to LLM
        ↓
Generate Final Answer
```

## 💬 Example Questions

```text
What is the annual leave policy?

What is the notice period for employees?

Who is eligible for maternity leave?

How many sick leaves are provided?

What are the working hours?

What is the company's work-from-home policy?
```

## 🧠 RAG Pipeline

The project uses **Retrieval-Augmented Generation (RAG)** rather than relying only on the LLM's pretrained knowledge.

The pipeline can be summarized as:

```text
Documents
    ↓
Chunking
    ↓
Embedding Model
    ↓
FAISS Vector Store
    ↓
Similarity Search
    ↓
Re-ranking
    ↓
Relevant Context
    ↓
LLM
    ↓
Final Answer
```

This allows the chatbot to answer questions using information contained in the uploaded HR documents.

## 📈 Future Improvements

* 🔐 JWT authentication
* 👥 Role-Based Access Control (RBAC)
* 🗄️ PostgreSQL integration
* ⚡ Redis caching
* ☁️ AWS deployment
* 🐳 Docker containerization
* 📊 Chat and query analytics
* 📁 Multi-document management
* 🔍 Hybrid search
* 🧾 Source citations for generated answers
* 💬 Conversation history
* 👨‍💼 Separate HR and employee access

## 🔒 Security Considerations

For production deployment:

* Store API keys in environment variables
* Do not commit `.env` files
* Validate uploaded files
* Restrict supported file types
* Implement authentication and authorization
* Add rate limiting
* Secure API endpoints
* Protect confidential HR documents

## 🎯 Project Objective

The main objective of this project is to build an intelligent HR document assistant that reduces the time required to search through large HR documents and provides users with quick, context-aware answers through natural language interaction.

## 👩‍💻 Author

**Bhavana R**




