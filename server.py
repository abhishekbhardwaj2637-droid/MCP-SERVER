from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import sys
import os

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(title="Google MCP Server")

API_KEY = os.environ.get("API_KEY")

async def verify_api_key(x_api_key: str = Header(None)):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

class AppendDocRequest(BaseModel):
    doc_id: str
    content: str

class EmailDraftRequest(BaseModel):
    to: str
    subject: str
    body: str

def ask_for_approval(action_name: str, payload: dict) -> bool:
    if os.environ.get("ENVIRONMENT") == "production":
        return True

    print(f"\n--- ACTION REQUIRED ---")
    print(f"Action: {action_name}")
    print(f"Payload: {payload}")
    
    # We use input() to pause the server and ask the user in the terminal
    # Note: In a real-world multi-user FastAPI app, this would block the thread.
    # Since this is a local tool server meant for a single user, it's acceptable.
    sys.stdout.flush()
    while True:
        try:
            choice = input("Approve? (y/n): ").strip().lower()
            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            else:
                print("Please enter 'y' or 'n'.")
        except EOFError:
            return False

@app.post("/append_to_doc", dependencies=[Depends(verify_api_key)])
def handle_append_to_doc(request: AppendDocRequest):
    payload = request.model_dump()
    if not ask_for_approval("Append to Google Doc", payload):
        raise HTTPException(status_code=403, detail="Action denied by user.")
    
    result = append_to_doc(request.doc_id, request.content)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@app.post("/create_email_draft", dependencies=[Depends(verify_api_key)])
def handle_create_email_draft(request: EmailDraftRequest):
    payload = request.model_dump()
    if not ask_for_approval("Create Gmail Draft", payload):
        raise HTTPException(status_code=403, detail="Action denied by user.")
    
    result = create_email_draft(request.to, request.subject, request.body)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
