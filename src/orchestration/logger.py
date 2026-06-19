import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'audit_log.txt')

def log_event(level: str, message: str):
    """Writes an audit log entry."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] [{level.upper()}] {message}\n"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
        
def log_info(message: str):
    log_event("INFO", message)
    print(f"INFO: {message}")
    
def log_error(message: str):
    log_event("ERROR", message)
    print(f"ERROR: {message}")

def log_success(message: str):
    log_event("SUCCESS", message)
    print(f"SUCCESS: {message}")

import json

def log_audit(audit_data: dict):
    """
    Appends a structured JSON audit log entry to data/audit.jsonl.
    """
    audit_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'audit.jsonl')
    os.makedirs(os.path.dirname(audit_file), exist_ok=True)
    
    with open(audit_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(audit_data) + '\n')

