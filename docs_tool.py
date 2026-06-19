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

def check_doc_anchor(doc_id: str, anchor: str) -> dict:
    """Checks if the document contains the specified anchor text."""
    try:
        creds = get_credentials()
        service = build("docs", "v1", credentials=creds)

        doc = service.documents().get(documentId=doc_id).execute()
        
        # Extract text from doc body
        text_content = ""
        for structural_element in doc.get('body', {}).get('content', []):
            if 'paragraph' in structural_element:
                for element in structural_element['paragraph'].get('elements', []):
                    if 'textRun' in element:
                        text_content += element['textRun'].get('content', '')
                        
        found = anchor in text_content
        return {"status": "success", "found": found}
        
    except HttpError as error:
        return {"status": "error", "message": str(error)}
