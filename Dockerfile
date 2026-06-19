FROM python:3.12-slim

# Install system dependencies (required for compiling UMAP/HDBSCAN if wheel is not available)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the spaCy model required for Presidio PII scrubber
RUN python -m spacy download en_core_web_sm

# Pre-download the SentenceTransformer model to speed up runtime starts
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the rest of the application files
COPY . .

# Expose port 8001 (configurable via PORT env var in run_app.py)
EXPOSE 8001

# Command to run the dashboard server
CMD ["python", "run_app.py"]
