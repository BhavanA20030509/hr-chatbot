# Use Python base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose backend and frontend ports
EXPOSE 8000
EXPOSE 8501

# Run backend + frontend together
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/chat_ui.py --server.port 8501 --server.address 0.0.0.0"]
