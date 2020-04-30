#!/usr/bin/env python

import gspread
import json
import os
import re
import requests

from webloc2csv import sanitize_title, get_url_tags, get_keyword_tags  # clean_url, extract_title_n_url, add_tags
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from pandas.io.clipboard import clipboard_get


# ----- Initialization -----
clipboard_txt = clipboard_get()
print(f'Clipboard text:\n{clipboard_txt}')


# ----- Helper Subroutines -----
def clipboard_to_url(clipboard_txt):
    """
    Returns url if the clipboard text starts with http
    otherwise, returns None
    """
    if clipboard_txt.startswith('http'):
        return clipboard_txt
    else:
        print('Clipboard content is not a url:')
        print(f'{clipboard_txt}')
        return None


def url_to_title(url):
    """
    Given a url, look up the HTML page
    and extract the title if possible
    Return the sanitized title
    """
    r = requests.get(url)
    html_txt = r.content.decode()
    soup = BeautifulSoup(html_txt, 'html5lib')
    if soup.title is None:
        title = '[Title not found]'
    else:
        title = soup.title.string

    # Sanitize title
    title = sanitize_title(title)
    title = re.sub('\n', ' • ', title).strip()
    return title


def get_tags(title, url):
    """
    Given a title and a URL, return tags.
    """
    tags1 = get_keyword_tags(title)
    tags2 = get_url_tags(url)
    tags = (tags1 + ' ' + tags2).strip()
    tags = ' '.join(set(tags.split(' ')))
    return tags


def append_worksheet_row(WS, values: list):
    """
    Appends a row to a Google Sheets worksheet
    """
    rows = WS.row_count
    try:
        WS.add_rows(1)
        for i, value in enumerate(values):
            WS.update_cell(rows+1, i+1, value)
    except gspread.exceptions.APIError as e:
        print(f'Error adding rows to worksheet: {e}')


def print_last_5_rows(WS):
    """
    Prints the last 5 rows of a Google Sheets worksheet
    """
    cell_data = WS.get_all_values()
    i_start = len(cell_data) - 5
    i_end = len(cell_data)

    for i, row_data in enumerate(cell_data):
        if i < i_start or i > i_end:
            continue
        print(f"{i}: {'|'.join(row_data)}")


def parse_clipboard(clipboard_txt):
    """
    Parses clipboard text into tags, title, url
    """
    url = clipboard_to_url(clipboard_txt)
    if url is None:
        return None, None, None

    title = url_to_title(url)
    print(f'Using title: {title}')

    tags = get_tags(url, title)
    print(f'Tags: {tags}')
    return tags, title, url


# ----- Load Parameters -----
SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(SCRIPT_FOLDER, 'google_sheets_bookmarks.json')) as f:
    params = json.load(f)

GDRIVE_CREDENTIALS = os.getenv('GDRIVE_CREDENTIALS', None)
GDRIVE_SPREADSHEET = params['GDRIVE_SPREADSHEET']
BOOKMARKS_SPREADSHEET_ID = params['BOOKMARKS_SPREADSHEET_ID']


# ----- Setup Google Sheets Link -----
if GDRIVE_CREDENTIALS:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filename=GDRIVE_CREDENTIALS,
        scopes=['https://www.googleapis.com/auth/drive'])
    GC = gspread.authorize(credentials)
    SH = GC.open(GDRIVE_SPREADSHEET)
    WS = SH.sheet1
else:
    WS = None


if __name__ == "__main__":
    tags, title, url = parse_clipboard(clipboard_txt)
    if title:
        append_worksheet_row(WS, values=[tags, title, url])
    else:
        print('Failed to parse clipboard')
    print_last_5_rows(WS)
