#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import PyPDF2
import re


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
    The DOI is extracted
    """
    d = pdf2text(filename)
    doi = txt2doi(d[0])
    if doi is not None:
        print(f'DOI = "{doi}"')
    else:
        print('No DOI found in the following text:')
        print(f'{d[0]}')
    return {
        'text': d,
        'doi': doi
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Text Extractor")
    parser.add_argument('file')
    args = parser.parse_args()
    parse_pdf(args.file)
