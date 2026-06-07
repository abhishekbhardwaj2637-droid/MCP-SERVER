# Google MCP Server

A FastAPI-based Model Context Protocol (MCP) style server that integrates with Google Docs and Gmail.

## Features
- **Append to Google Doc**: Appends text to the end of a specified Google Document.
- **Create Gmail Draft**: Creates an email draft in your Gmail account.
- **Terminal Approval**: Prompts for user approval (`y/n`) in the terminal before executing any action.

## Prerequisites
1. Python 3.8+
2. A Google Cloud Project with the following APIs enabled:
   - Google Docs API
   - Gmail API
3. OAuth 2.0 Client IDs configured in your Google Cloud Project.
4. Download the OAuth client JSON file and save it as `credentials.json` in this directory.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn server:app --reload
   ```

On the first run, a browser window will open to authorize the application. Once authorized, a `token.json` file will be created locally.

## API Endpoints

### 1. Append to Google Doc
**Endpoint:** `POST /append_to_doc`

**Payload:**
```json
{
  "doc_id": "your_google_doc_id",
  "content": "Text to append"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/append_to_doc \
  -H "Content-Type: application/json" \
  -d '{"doc_id": "xyz123...", "content": "\nHello World"}'
```

### 2. Create Email Draft
**Endpoint:** `POST /create_email_draft`

**Payload:**
```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body content"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/create_email_draft \
  -H "Content-Type: application/json" \
  -d '{"to": "test@example.com", "subject": "Test Draft", "body": "This is a test draft."}'
```
