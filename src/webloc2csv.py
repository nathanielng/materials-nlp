#!/usr/bin/env python

# Description:
# - Parses a folder containing .webloc files
# - Exports filename & url to a .csv
#
# Requirements:
# ```
# pip install pygsheets webloc
# ```

import argparse
import glob
import json
import os
import pandas as pd
import pygsheets
import re
import webloc


def clean_url(url):
    m = re.match('([^?]*)', url)
    if m is None:
        return url
    else:
        return m.group(1)


def sanitize_title(title):
    title = re.sub('[?]', '', title)
    title = re.sub('[‘’"]', "'", title)
    title = re.sub('…', '...', title)
    title = re.sub('[—|*]','-', title)
    return title.strip()


def extract_title_n_url(filename, rename=True):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    title, ext = os.path.splitext(basename)
    if ext == '.webloc':
        url = webloc.read(filename)
        clean_title = sanitize_title(title)
        if rename is True:
            new_filename = f"{dirname}/{clean_title}.webloc"
            if filename != new_filename:
                print(f"{filename} -> {new_filename}")
                os.rename(filename, new_filename)
        return {
            'Title': clean_title,
            'Original url': url 
        }
    else:
        return None


def get_url_tags(url):
    tag_set = set()
    for tg, regex in tag_urls.items():
        m = re.search(regex, url, re.IGNORECASE)
        if m is not None:
            tag_set.add(tg)
    tags = ' '.join(tag_set)
    return tags.strip()


def get_keyword_tags(title):
    tag_set = set()
    for tg, regex in tag_keywords.items():
        m = re.search(regex, title, re.IGNORECASE)
        if m is not None:
            tag_set.add(tg)
    tags = ' '.join(tag_set)
    return tags.strip()


def add_tags(df):
    df['tags1'] = df['Title'].apply(get_keyword_tags)
    df['tags2'] = df['url'].apply(get_url_tags)
    df['tags'] = df['tags1'] + ' ' + df['tags2']
    df['tags'] = df['tags'].apply(
        lambda x: ' '.join(sorted(set(x.split(' ')))).strip()
    )
    df = df.drop(labels=['tags1', 'tags2'], axis=1)
    return df


def bookmarkfolder2df(folder, clean_urls=True):
    bookmarks = []
    files = glob.glob(f"{folder}/*.webloc")
    if len(files) == 0:
        print(f"No files found in {folder}")
        return None

    for file in files:
        d = extract_title_n_url(file)
        if d is not None:
            bookmarks.append(d)

    df = pd.DataFrame(bookmarks)
    df['tags'] = ''
    if clean_urls is True:
        df['url'] = df['Original url'].apply(clean_url)
        df = df[['tags', 'Title', 'url', 'Original url']]
    else:
        df = df[['tags', 'Title', 'Original url']]
    return df


def print_untagged(df):
    untagged = df['tags'].str.len() == 0
    pd.set_option('max_rows', 100)
    pd.set_option('max_colwidth', 80)
    print('----- Untagged -----')
    print(df.loc[untagged, ['tags', 'Title']])

    untagged_count = (untagged).sum()
    print(f'Untagged rows: {untagged_count}')


def save_df(df, dest, cols=['tags', 'Title', 'url']):
    if dest is None:
        outfile = 'my_bookmarks.csv'
    else:
        outfile = dest

    filename, ext = os.path.splitext(outfile)
    if ext == '.csv':
        print(f"Exporting {len(df)} bookmarks to {outfile}")
        print('Sorting dataframe by tags')
        df = df.sort_values('tags').reset_index(drop=True)
        df[cols].to_csv(outfile, index=False)
    else:
        print(f'Invalid filename extension: {ext}')


def bookmarkfolder2file(path, dest):
    """
    Loads a folder of .webloc files
    """
    folder = os.path.abspath(path)
    print(f'Loading bookmarks from {folder}')
    df = bookmarkfolder2df(folder)
    if df is None:
        return
    df = add_tags(df)
    save_df(df, dest)
    print(f"Saved bookmarks to: '{dest}'")
    # print_untagged(df.head())
    return df


def append_df(work_sheet, df):
    """
    Appends a data frame to a worksheet
    """
    n_rows = work_sheet.rows
    # work_sheet.add_rows(len(df))
    work_sheet.set_dataframe(
        df, start=n_rows, copy_index=False, copy_head=False, fit=True)


def upload_df_to_gdrive(df):
    if ws is None:
        return

    upload_to_gdrive = input('Upload to Google Drive (y/n)? ')
    if upload_to_gdrive[:1].lower() != 'y':
        return

    append_df(ws, df)


# ----- Load Parameters -----
SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(SCRIPT_FOLDER, 'tag_keywords.json')) as f:
    tag_keywords = json.load(f)

with open(os.path.join(SCRIPT_FOLDER, 'tag_urls.json')) as f:
    tag_urls = json.load(f)

with open(os.path.join(SCRIPT_FOLDER, 'google_sheets_bookmarks.json')) as f:
    params = json.load(f)

GDRIVE_CREDENTIALS = os.getenv('GDRIVE_CREDENTIALS', None)
GDRIVE_SPREADSHEET = params['GDRIVE_SPREADSHEET']
BOOKMARKS_SPREADSHEET_ID = params['BOOKMARKS_SPREADSHEET_ID']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--output', default='tagged_bookmarks.csv')
    args = parser.parse_args()

    if args.path.endswith('.csv'):
        print(f'The .csv file {args.path} will be tagged')
        df = pd.read_csv(args.path)
        print(df.columns)
        df['Title'] = df['Title'].astype(str)
        df['url'] = df['url'].astype(str)
        df = add_tags(df)
        save_df(df, dest=args.output, cols=['tags', 'Title', 'url'])
        print_untagged(df)
        upload_df_to_gdrive(df)
    else:
        print(f'The files in folder {args.path} will be tagged')
        df = bookmarkfolder2file(args.path, args.output)
        # upload_df_to_gdrive(df)
