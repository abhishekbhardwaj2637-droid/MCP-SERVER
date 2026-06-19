import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth import get_credentials

def create_email_draft(to: str, subject: str, body: str) -> dict:
    """Creates an email draft in the user's Gmail account."""
    try:
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["Subject"] = subject

        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"message": {"raw": encoded_message}}

        draft = service.users().drafts().create(
            userId="me", body=create_message
        ).execute()

        return {"status": "success", "draft_id": draft["id"]}

    except HttpError as error:
        return {"status": "error", "message": str(error)}

def send_email(to: str, subject: str, body: str) -> dict:
    """Sends an email from the user's Gmail account."""
    try:
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["Subject"] = subject

        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        sent_message = service.users().messages().send(
            userId="me", body=create_message
        ).execute()

        return {"status": "success", "message_id": sent_message["id"]}

    except HttpError as error:
        return {"status": "error", "message": str(error)}

def check_email_sent(subject: str) -> dict:
    """Checks if an email with the specified subject has been sent."""
    try:
        creds = get_credentials()
        service = build("gmail", "v1", credentials=creds)

        # Search for sent messages matching the subject
        query = f"subject:{subject} in:sent"
        response = service.users().messages().list(userId="me", q=query).execute()
        
        messages = response.get("messages", [])
        found = len(messages) > 0
        
        return {"status": "success", "found": found}

    except HttpError as error:
        return {"status": "error", "message": str(error)}
