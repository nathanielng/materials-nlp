#!/usr/bin/env python

# Requirements:
# ```
# pip install webloc
# ```

import argparse
import os
import pandas as pd
import re
import webloc


def clean_url(url):
    m = re.match('([^?]*)', url)
    if m is None:
        return url
    else:
        return m.group(1)


def extract_title_n_url(filename):
    basename = os.path.basename(filename)
    title, ext = os.path.splitext(basename)
    if ext == '.webloc':
        url = webloc.read(filename)
        return {
            'Title': title,
            'Original url': url
        }
    else:
        return None


def bookmarkfolder2df(folder, clean_urls=True):
    bookmarks = []
    files = os.listdir(folder)
    for file in files:
        d = extract_title_n_url(file)
        if d is not None:
            bookmarks.append(d)

    df = pd.DataFrame(bookmarks)
    if clean_urls is True:
        df['url'] = df['Original url'].apply(clean_url)
        df = df[['Title', 'url', 'Original url']]
    return df


def bookmarkfolder2file(path, dest):
    folder = os.path.abspath(path)
    df = bookmarkfolder2df(folder)
    if dest is None:
        outfile = 'my_bookmarks.csv'
    else:
        outfile = args.output
    filename, ext = os.path.splitext(outfile)
    if ext == '.csv':
        print(f"Exporting bookmarks to {outfile}")
        df.to_csv(outfile)
    else:
        print(filename, ext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    bookmarkfolder2file(args.path, args.output)
