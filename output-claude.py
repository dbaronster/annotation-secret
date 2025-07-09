from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def read_google_doc(document_id):
    creds = google.auth.default()
    service = build('docs', 'v1', credentials=creds)

    document = service.documents().get(documentId=document_id).execute()
    content = document.get('body').get('content')

    full_text = []
    for element in content:
        if 'paragraph' in element:
            paragraph_elements = element.get('paragraph').get('elements')
            for text_run in paragraph_elements:
                if 'textRun' in text_run:
                    full_text.append(text_run.get('textRun').get('content'))
    return "".join(full_text)

# Replace 'YOUR_DOCUMENT_ID' with the actual ID of your Google Doc
# doc_text = read_google_doc('YOUR_DOCUMENT_ID')
# print(doc_text)