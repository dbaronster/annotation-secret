"""
ouput-json.py (Python 2.x or 3.x)
Google Docs (REST) API output-json sample app
"""
# [START output_json_python]
import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from oauth2client import client
from oauth2client import file
from oauth2client import tools
                                                                                            
# Set doc ID, as found at `https://docs.google.com/document/d/YOUR_DOC_ID/edit`
#DOCUMENT_ID = "2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq"
#DOCUMENT_ID = "1Lvw3M9tucSJrIorzx9YuSeYg79wk4e2FxaX9-yHKxFE"
DOCUMENT_ID_F = "1ppvMBTBedsQOzplR_8WN4CQKgJv6wJSTFpAHenHvCqY"
DOCUMENT_ID = '1wISxQ_i3J-VXFO8PLxjCTeJIvh6QkL9Dtfh-oFvRJ0I'
# Set the scopes and discovery info
SCOPES = "https://www.googleapis.com/auth/documents"
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/documents.readonly', 'https://www.googleapis.com/auth/drive']
 
DISCOVERY_DOC = "https://docs.googleapis.com/$discovery/rest?version=v1"

# Initialize credentials and instantiate Docs API service
#creds, _ = google.auth.default()
store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
  creds = tools.run_flow(flow, store)
# pylint: disable=maybe-no-member
try:
  service = build("docs", "v1", credentials = creds)

  # Do a document "get" request and print the results as formatted JSON

  result = service.documents().get(documentId=DOCUMENT_ID).execute()
  print(json.dumps(result, indent=4, sort_keys=True))
except HttpError as error:
  print(f"An error occurred: {error}")

# [END output_json_python]