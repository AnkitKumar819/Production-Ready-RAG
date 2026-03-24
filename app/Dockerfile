FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads vectorstore

EXPOSE 8000 8501

# Start only FastAPI (remove Streamlit for now to avoid crashes)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]