import os
import json
from datetime import datetime
from src.delivery.mcp_client import check_doc_anchor, check_email_sent

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'state.json')

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"processed_weeks": []}

def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def is_week_processed(week_str: str) -> bool:
    """
    Checks if the given ISO week string (e.g. '2026-W22') has already been processed.
    It verifies both the presence in Google Docs and the existence of a sent Gmail email.
    """
    # 1. Check Google Docs for the anchor
    doc_anchor = f"Week {week_str}"
    doc_processed = check_doc_anchor(doc_anchor)
    
    # 2. Check Gmail for the sent email
    # Assuming standard subject line: "Weekly Product Review Pulse - <week_str>"
    subject = f"Weekly Product Review Pulse - {week_str}"
    email_processed = check_email_sent(subject)
    
    if doc_processed or email_processed:
        print(f"Idempotency check: week {week_str} already processed (Doc: {doc_processed}, Email: {email_processed})")
        return True
        
    return False

def mark_week_processed(week_str: str):
    """
    Marks the ISO week string as successfully processed locally.
    This is kept for local state keeping although MCP provides source-of-truth.
    """
    state = load_state()
    if week_str not in state["processed_weeks"]:
        state["processed_weeks"].append(week_str)
        save_state(state)
