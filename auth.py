import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/gmail.compose"
]

def get_credentials():
    """Gets valid user credentials from storage or initiates OAuth2 flow."""
    creds = None
    
    token_json = os.environ.get("GOOGLE_TOKEN_JSON")
    if token_json:
        creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
            if credentials_json:
                flow = InstalledAppFlow.from_client_config(json.loads(credentials_json), SCOPES)
            else:
                if not os.path.exists("credentials.json"):
                    raise FileNotFoundError("credentials.json not found. Please download it from the Google Cloud Console.")
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            
            # Note: run_local_server will fail in production since there's no browser.
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run if not in production
        if os.environ.get("ENVIRONMENT") != "production":
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            
    return creds
