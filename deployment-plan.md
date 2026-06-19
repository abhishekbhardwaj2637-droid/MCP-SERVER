# Unified Production Deployment Plan

This document outlines the deployment strategy for the complete **Weekly Product Review Pulse** ecosystem, including:
1. **Google MCP Server:** Exposes Google Workspace API tools (Docs/Gmail) secured via API tokens.
2. **Weekly Pulse Dashboard & Scraper Pipeline:** The review processing engine and dynamic dashboard interface.

---

## Part 1: Google MCP Server Deployment (Railway)

Deploying the local Google MCP Server to Railway requires setting up authentication parameters and bypassing interactive terminal confirmations.

### 1. Remove Terminal Confirmation
In production, endpoint actions are auto-approved. Secure requests by generating an `API_KEY` that clients must provide in their headers.
- Set the environment variable `ENVIRONMENT=production` to bypass terminal prompts.
- Ensure clients provide the `X-API-Key` matching the server's configured `API_KEY`.

### 2. Configure Credentials as Environment Variables
Instead of committing `credentials.json` and `token.json` (which are ignored by git), paste their raw content strings directly into your Railway project environment:
- `GOOGLE_CREDENTIALS_JSON`: The contents of `credentials.json`.
- `GOOGLE_TOKEN_JSON`: The contents of `token.json`.

### 3. Railway Configuration
- Railway will inject a dynamic `$PORT` environment variable that the server automatically binds to.
- Select **Deploy from GitHub** on Railway and link the repository.
- Configure these variables:
  - `ENVIRONMENT`: `production`
  - `API_KEY`: `<your_secret_auth_token>`
  - `GOOGLE_CREDENTIALS_JSON`: `<raw string>`
  - `GOOGLE_TOKEN_JSON`: `<raw string>`

---

## Part 2: Dashboard & Scraper Pipeline Deployment (Docker - Option B)

We containerize the pipeline and web server to pre-cache heavy machine learning models (spaCy and sentence-transformers) at build-time to optimize server memory and reduce runtime start latency.

### 1. Dockerfile
Use the configured `Dockerfile` in the repository root:
```dockerfile
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download spaCy model for PII scrubber
RUN python -m spacy download en_core_web_sm

# Pre-download SentenceTransformer model to speed up runtime starts
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the rest of the application files
COPY . .

# Expose port 8001 (configurable via PORT env var in run_app.py)
EXPOSE 8001

CMD ["python", "run_app.py"]
```

### 2. Configure Cloud Web Service (Railway/Render)
1. Push the updated codebase to your GitHub repository.
2. In the cloud dashboard, select "Create New Web Service" and link to this repository.
3. Configure the following environment variables:
   - `PORT`: `8001` (Or let the system assign a dynamic port)
   - `GEMINI_API_KEY`: `<your_gemini_api_key>`
   - `MCP_SERVER_URL`: `https://your-mcp-server.railway.app` (The URL of the server deployed in Part 1)
   - `MCP_API_KEY`: `<your_mcp_server_api_key>`
   - `GOOGLE_DOC_ID`: `<target_google_doc_id>`
   - `STAKEHOLDER_EMAIL`: `<recipient_email>`
   - `MAX_REVIEWS_TO_FETCH`: `1000`
4. Deploy the service. The build engine will install requirements, cache models, compile C extensions, and expose the dashboard on the public URL.

---

## Part 3: Dashboard & Scraper Pipeline Deployment (Local VM - Option A)

If you prefer to deploy on a local dedicated Windows/Linux VM instead of Docker:
1. Clone the repository and configure `.env`.
2. Set up `run_app.py` as a system service using **NSSM** (Windows) or **systemd** (Linux).
3. Set up a weekly scheduler trigger (using **Windows Task Scheduler** or **cron** on Linux) to run `main.py` automatically (e.g. `0 9 * * 1` for Monday at 9:00 AM IST).
