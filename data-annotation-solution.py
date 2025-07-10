# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pip._vendor.urllib3.packages.six import print_

"""
Recursively extracts the text from a Google Doc.
"""
import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import json
import string

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

                                                                                            
# Set doc ID, as found at `https://docs.google.com/document/d/YOUR_DOC_ID/edit`
#DOCUMENT_ID = "1Lvw3M9tucSJrIorzx9YuSeYg79wk4e2FxaX9-yHKxFE"
DOCUMENT_ID_F = "1ppvMBTBedsQOzplR_8WN4CQKgJv6wJSTFpAHenHvCqY"
DOCUMENT_ID_LOCAL = '1wISxQ_i3J-VXFO8PLxjCTeJIvh6QkL9Dtfh-oFvRJ0I'
DOCUMENT_ID_FAIL = '2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A'
DOCUMENT_ID = DOCUMENT_ID_LOCAL

# Set the scopes and discovery info
SCOPES = "https://www.googleapis.com/auth/documents"
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/documents.readonly', 'https://www.googleapis.com/auth/drive']
 
DISCOVERY_DOC = "https://docs.googleapis.com/$discovery/rest?version=v1"



def get_credentials():
  """Gets valid user credentials from storage.

  If nothing has been stored, or if the stored credentials are invalid,
  the OAuth 2.0 flow is completed to obtain the new credentials.

  Returns:
      Credentials, the obtained credential.
  """
  store = file.Storage('token.json')
  credentials = store.get()

  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    credentials = tools.run_flow(flow, store)
  return credentials

import html

def dict_to_html_table(num_rows, num_cols, dictionary):
    
    html_table = '<!DOCTYPE html><html lang="en"><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head>'
    html_table += '<table><tbody>'
    
    for row in range(num_rows):
        html_table += '<tr>'
        for col in range(num_cols):
            html_table += '<td>'
            try:
                html_table += dictionary[str(num_rows - row - 1)][str(col)]
            except:
                html_table += '&nbsp;'
            html_table += '</td>'
        html_table += '</tr>'
    html_table += '</tbody></table>'
    html_table += '</html>'
    return html_table


def print_dict_to_console(num_rows, num_cols, dictionary):
    
    for row in range(num_rows):
        line_text = ''
        for col in range(num_cols):
            try:
                line_text += dictionary[str(num_rows - row - 1)][str(col)]
            except:
                line_text += ' '
        print(line_text)


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.
    
    Args:
      element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def decode_table_secret(table):
    """Traverses a table structured as described in the 
    DataAnnotation Coding Exercise: Decoding a Secret Message

    
    Args:
    table: a document element of type 'table'.
    """

    tabledict = {}
    x_max = 0
    y_max = 0
    skipped_first = False
    for row in table.get('tableRows'):
        if (not skipped_first):
            skipped_first = True
        else:
            cells = row.get('tableCells')
            """Grab the 0-2 cells from the row"""
            x_coordinate = read_structural_elements(cells[0].get('content'))
            cell_unicode = read_structural_elements(cells[1].get('content'))
            y_coordinate = read_structural_elements(cells[2].get('content'))
            if (int(x_coordinate) > x_max):
                x_max = int(x_coordinate)
            if (int(y_coordinate) > y_max):
                y_max = int(y_coordinate)
            #print(f"{x_coordinate} {cell_unicode} {y_coordinate} ")
            coldict = {x_coordinate:cell_unicode}
            if (y_coordinate in tabledict):
                rowdict = tabledict.get(y_coordinate)
                rowdict.update(coldict)
            else:
                tabledict[y_coordinate] = coldict
    #print(f"dimensions: {y_max}x{x_max} dist: {tabledict}")
    #html_table = dict_to_html_table(y_max+1, x_max+1, tabledict)
    #print(html_table)
    print_dict_to_console(y_max+1, x_max+1, tabledict)


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text
    where text may be in nested elements.
    
    Args:
    elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem).removesuffix('\n')
        elif 'table' in value:
            table = value.get('table')
            decode_table_secret(table)

        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def main():
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
        #print(json.dumps(result, indent=4, sort_keys=True))

        doc_content = result.get('body').get('content')
        """Use the Docs API to extract the text of a document."""
        print(read_structural_elements(doc_content))
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
  main()
