#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import requests
import glob
import os
import PyPDF2
import re

from xml.etree.ElementTree import fromstring


# ----- Crossref -----
def get_doi_metadata(doi):
    url = f'http://api.crossref.org/works/{doi}'
    r = requests.get(url)
    if r.ok is False:
        print(f'DOI: {doi} lookup returned {r.status_code}')
        return None
    data = r.json()
    if 'message' in data.keys():
        return data['message']
    else:
        return None


def extract_title(data):
    if 'title' in data:
        title = data['title']
        if len(title) > 0:
            return title[0]
    return None


# ----- ArXiv -----
def convert_arxiv_url(url):
    """
    Converts a URL from
    https://arxiv.org/abs/0000.00000
    to
    https://arxiv.org/pdf/0000.00000.pdf
    """
    return re.sub(r'/abs/', '/pdf/', url) + '.pdf'


def arxiv2pdf(url):
    """
    Downloads the PDF associated with a URL of the format
    https://arxiv.org/abs/0000.00000

    Note that PDF access with a 15 seconds delay between
    requests appears permitted according to:
    https://arxiv.org/robots.txt

    This subroutine should not be used for bulk downloading. See:
    https://arxiv.org/help/robots
    """
    pdf_url = convert_arxiv_url(url)
    response = requests.get(pdf_url, allow_redirects=True)
    if response.status_code != 200:
        print(f'Failed to download PDF from {pdf_url}')
        return
    filename = re.sub(r'.*/', '', url) + '.pdf'
    with open(filename, 'wb') as f:
        f.write(response.content)


def get_arxiv_metadata(arxiv_id):
    """
    Retrieves the metadata associated with an arXiv ID of the form
    0000.00000
    """
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    response = requests.get(url)
    root = fromstring(response.text)
    for child in root:
        if child.tag.endswith('entry'):
            entry = {}
            author_list = []
            for e in child:
                tag = re.sub(r'\{.*\}', '', e.tag)
                if tag == 'author':
                    author_list += [a.text for a in e.getchildren()]
                else:
                    entry[tag] = e.text
            entry['author'] = author_list
    return entry


def txt2doi(txt):
    """
    Extract a DOI from text data
    """
    regex = r'(https?://)?dx\.doi\.org/([0-9.]+/[A-Za-z0-9.]+)'
    m = re.search(regex, txt)
    if m is not None:
        return m.group(0), m.group(2)
    else:
        return None, None


def detect_arxiv(txt):
    """
    Extract an arXiv ID from text data
    """
    regex = r'arXiv:[0-9]{4,4}\.[0-9]{5,5}(v[0-9]+)?'
    m = re.search(regex, txt)
    if m is not None:
        return m.group(0)
    else:
        return None


# ----- PDF File Processing -----
def pdf2text(filename):
    """
    Extracts text from a PDF document using PyPDF2
    """
    with open(filename, 'rb') as f:
        pdf_obj = PyPDF2.PdfFileReader(f)
        d = {}
        for i in range(pdf_obj.numPages):
            d[i] = pdf_obj.getPage(i).extractText()
    return d


def parse_pdf(filename):
    """
    Parses a PDF file
    Returns a dictionary of text from each page
    and if available, the DOI of the article
    """
    page_data = pdf2text(filename)
    doi_url, doi = txt2doi(page_data[0])  # extract doi from first page
    return {
        'text': page_data,
        'doi': doi
    }


# ----- File & Folder Handling -----
def get_file_list(path):
    """
    Gets the list of files in a given path
    """
    os.chdir(os.path.abspath(path))
    return glob.glob(f'*.pdf')


def parse_file(file):
    d = parse_pdf(file)
    doi = d['doi']
    page_data = d['text']
    if doi is not None:
        print(f'DOI = "{doi}"')
    else:
        print('No DOI found in the following text:')
        print(f'{page_data[0]}')


def parse_folder(path):
    file_list = get_file_list(path)
    print(f'PDF files in folder: {path}')
    for i, file in enumerate(file_list):
        d = parse_pdf(file)
        doi = d['doi']
        if doi is None:
            print(f'{i}: {file}')
            continue
        print(f'{i}: {file} (doi={doi})')
        data = get_doi_metadata(doi)
        if data is None:
            continue
        title = extract_title(data)
        if title is not None:
            newname = f'{title}.pdf'
            ans = input(f"Rename {file} to {newname} (Y/N)? ")
            if ans[0].upper() == 'Y':
                newname = re.sub(r'[:/]', '-', newname)
                os.rename(file, newname)


def main(args):
    if isinstance(args.path, str):
        parse_folder(args.path)
    else:
        parse_file(args.file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Text Extractor")
    parser.add_argument('--path', default=None)
    parser.add_argument('--file')
    args = parser.parse_args()
    main(args)
