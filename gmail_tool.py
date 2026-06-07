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
