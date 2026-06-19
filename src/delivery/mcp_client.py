import os
import requests
from dotenv import load_dotenv

load_dotenv()

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://web-production-c2c29.up.railway.app").rstrip("/")

def get_headers() -> dict:
    api_key = os.getenv("MCP_API_KEY")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key
    return headers

def deliver_to_docs(content: str) -> bool:
    """
    Sends the generated plain text report to the unified MCP server
    to be appended to the target Google Doc.
    """
    doc_id = os.getenv("GOOGLE_DOC_ID")
    if not doc_id:
        print("WARNING: GOOGLE_DOC_ID not set in .env. Skipping Google Docs delivery.")
        return False
        
    endpoint = f"{MCP_SERVER_URL}/append_to_doc"
    payload = {
        "doc_id": doc_id,
        "content": content
    }
    
    print(f"Delivering report to Google Doc via MCP Server: {endpoint}...")
    try:
        response = requests.post(endpoint, json=payload, headers=get_headers())
        response.raise_for_status()
        print("Successfully appended report to Google Doc.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with MCP server for Google Docs: {e}")
        if e.response is not None:
            print(f"Server response: {e.response.text}")
        return False

def deliver_to_gmail(content: str, subject: str = "Weekly Product Review Pulse") -> bool:
    """
    Sends the generated HTML report to the unified MCP server
    to send an email via Gmail.
    """
    to_email = os.getenv("STAKEHOLDER_EMAIL")
    if not to_email:
        print("WARNING: STAKEHOLDER_EMAIL not set in .env. Skipping Gmail delivery.")
        return False
        
    endpoint = f"{MCP_SERVER_URL}/send_email"
    payload = {
        "to": to_email,
        "subject": subject,
        "body": content
    }
    
    print(f"Sending Email via MCP Server: {endpoint}...")
    try:
        response = requests.post(endpoint, json=payload, headers=get_headers())
        response.raise_for_status()
        print("Successfully sent email.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with MCP server for Gmail: {e}")
        if e.response is not None:
            print(f"Server response: {e.response.text}")
        return False

def check_doc_anchor(anchor: str) -> bool:
    """
    Checks if a specific anchor text exists in the Google Doc via the MCP server.
    Returns True if it exists, False otherwise.
    """
    doc_id = os.getenv("GOOGLE_DOC_ID")
    if not doc_id:
        print("WARNING: GOOGLE_DOC_ID not set in .env. Skipping Google Docs anchor check.")
        return False
        
    endpoint = f"{MCP_SERVER_URL}/check_doc_anchor"
    payload = {
        "doc_id": doc_id,
        "anchor": anchor
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=get_headers())
        response.raise_for_status()
        data = response.json()
        return data.get("found", False)
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with MCP server for Docs anchor check: {e}")
        return False

def check_email_sent(subject: str) -> bool:
    """
    Checks if a Gmail email with the specific subject has been sent via the MCP server.
    Returns True if it exists, False otherwise.
    """
    endpoint = f"{MCP_SERVER_URL}/check_email_sent"
    payload = {
        "subject": subject
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=get_headers())
        response.raise_for_status()
        data = response.json()
        return data.get("found", False)
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with MCP server for Gmail sent check: {e}")
        return False
