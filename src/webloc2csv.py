#!/usr/bin/env python

# Requirements:
# ```
# pip install webloc
# ```

import argparse
import glob
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


def sanitize_title(title):
    title = re.sub('[?]', '', title)
    title = re.sub('[‘’"]', "'", title)
    title = re.sub('…', '...', title)
    title = re.sub('[—|*]','-', title)
    return title


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


tag_substitution = {
    ' #cloud': r'(aws|azure|ec2|google cloud)',
    ' #data_science': '(data science|data scientist|pandas|bias.variance|latent dirichlet allocation|regression|rmarkdown|statistics|time.series)',
    ' #deep_learning': r'(deep learning|keras|pytorch|tensorflow)',
    ' #devops': r'docker',
    ' #materials': r'(material|manufacturing)',
    ' #math': r'math',
    ' #ml': r'(A\.I\.| AI |^AI |machine learning|kaggle|fast.ai|iclr|neural network|gradient descent)',
    ' #physics': r'physics',
    ' #python': r'(python|pandas)',
    ' #reinforcement_learning': r'(reinforcement learning)',
    ' #research': r'(academia|arxiv|phd|research)',
    ' #web': r'(bootstrap|css|html)'
}

def add_tags(df):
    for idx, data in df.iterrows():
        tag = data['tags']
        title = data['Title']
        url = data['url']

        m = re.search('github', url, re.IGNORECASE)
        if m is not None:
            tag += ' #github'
        
        for tg, regex in tag_substitution.items():
            m = re.search(regex, title, re.IGNORECASE)
            if m is not None:
                tag += tg        
        df.loc[idx, 'tags'] = tag
    return df


def bookmarkfolder2file(path, dest):
    folder = os.path.abspath(path)
    df = bookmarkfolder2df(folder)
    if df is None:
        return
    df = add_tags(df)
    print(df[['tags', 'Title']].head(20))
    if dest is None:
        outfile = 'my_bookmarks.csv'
    else:
        outfile = args.output
    filename, ext = os.path.splitext(outfile)
    if ext == '.csv':
        print(f"Exporting {len(df)} bookmarks to {outfile}")
        df.to_csv(outfile)
    else:
        print(filename, ext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    bookmarkfolder2file(args.path, args.output)
