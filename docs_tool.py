from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth import get_credentials

def append_to_doc(doc_id: str, content: str) -> dict:
    """Appends content to the end of a Google Doc."""
    try:
        creds = get_credentials()
        service = build("docs", "v1", credentials=creds)

        requests = [
            {
                'insertText': {
                    'endOfSegmentLocation': {
                        'segmentId': ''  # empty string means document body
                    },
                    'text': content
                }
            }
        ]

        result = service.documents().batchUpdate(
            documentId=doc_id, body={'requests': requests}).execute()
        
        return {"status": "success", "result": result}
        
    except HttpError as error:
        return {"status": "error", "message": str(error)}
