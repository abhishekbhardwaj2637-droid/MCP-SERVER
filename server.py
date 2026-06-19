from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import sys
import os

from docs_tool import append_to_doc, check_doc_anchor
from gmail_tool import send_email, check_email_sent

app = FastAPI(title="Google MCP Server")

API_KEY = os.environ.get("API_KEY")

async def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

class AppendDocRequest(BaseModel):
    doc_id: str
    content: str

class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str

class CheckDocAnchorRequest(BaseModel):
    doc_id: str
    anchor: str

class CheckEmailSentRequest(BaseModel):
    subject: str

def ask_for_approval(action_name: str, payload: dict) -> bool:
    # Auto-approve actions without prompting the terminal
    print(f"\n--- AUTO-APPROVED ACTION ---")
    print(f"Action: {action_name}")
    print(f"Payload: {payload}")
    return True

@app.post("/append_to_doc", dependencies=[Depends(verify_api_key)])
def handle_append_to_doc(request: AppendDocRequest):
    payload = request.model_dump()
    if not ask_for_approval("Append to Google Doc", payload):
        raise HTTPException(status_code=403, detail="Action denied by user.")
    
    result = append_to_doc(request.doc_id, request.content)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@app.post("/send_email", dependencies=[Depends(verify_api_key)])
def handle_send_email(request: SendEmailRequest):
    payload = request.model_dump()
    if not ask_for_approval("Send Email via Gmail", payload):
        raise HTTPException(status_code=403, detail="Action denied by user.")
    
    result = send_email(request.to, request.subject, request.body)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@app.post("/check_doc_anchor", dependencies=[Depends(verify_api_key)])
def handle_check_doc_anchor(request: CheckDocAnchorRequest):
    result = check_doc_anchor(request.doc_id, request.anchor)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.post("/check_email_sent", dependencies=[Depends(verify_api_key)])
def handle_check_email_sent(request: CheckEmailSentRequest):
    result = check_email_sent(request.subject)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
