#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import glob
import os
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
            print(f'{i}: {file}')
    else:
        parse_pdf(args.file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF Text Extractor")
    parser.add_argument('--path', default=None)
    parser.add_argument('--file')
    args = parser.parse_args()
    main(args)
