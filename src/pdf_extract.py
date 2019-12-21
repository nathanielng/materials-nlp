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


def txt2doi(txt):
    """
    Extract a DOI from text data
    """
    regex = r'(https?://)?dx\.doi\.org/[0-9.]+/[A-Za-z0-9.]+'
    m = re.search(regex, txt)
    if m is not None:
        return m.group(0)
    else:
        return None


def parse_pdf(filename):
    """
    Parses a PDF file
    Returns a dictionary of text from each page
    and if available, the DOI of the article
    """
    page_data = pdf2text(filename)
    doi = txt2doi(page_data[0])  # extract doi from first page
    return {
        'text': page_data,
        'doi': doi
    }


def get_file_list(path):
    """
    Gets the list of files in a given path
    """
    os.chdir(os.path.abspath(path))
    return glob.glob(f'*.pdf')


def main(args):
    if isinstance(args.path, str):
        file_list = get_file_list(args.path)
        print(f'PDF files in folder: {args.path}')
        for i, file in enumerate(file_list):
            d = parse_pdf(file)
            doi = d['doi']
            if doi is None:
                print(f'{i}: {file}')
            else:
                print(f'{i}: {file} (doi={doi})')
    else:
        d = parse_pdf(args.file)
        doi = d['doi']
        page_data = d['text']
        if doi is not None:
            print(f'DOI = "{doi}"')
        else:
            print('No DOI found in the following text:')
            print(f'{page_data[0]}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Text Extractor")
    parser.add_argument('--path', default=None)
    parser.add_argument('--file')
    args = parser.parse_args()
    main(args)
