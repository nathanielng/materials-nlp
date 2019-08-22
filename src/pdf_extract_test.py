#!/usr/bin/env python

import pdf_extract
import pytest


def test_txt2doi():
    txt = """
    This is some text containing a doi:
    Here is a doi http://dx.doi.org/10.1234/123.456.789 that should be detected.
    This is the last line of text.
    """
    assert pdf_extract.txt2doi(txt) == "http://dx.doi.org/10.1234/123.456.789"
