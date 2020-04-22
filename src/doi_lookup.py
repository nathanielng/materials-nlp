#!/usr/bin/env python

# Looks up the metadata of a DOI
import argparse
import json
import requests


def url_to_json(url):
    r = requests.get(url)
    if r.ok is False:
        print(f'r.ok = {r.ok}')
        print(f'Response: {r}')
        return None
    return r.json()


# ----- Crossref -----
def get_author_list(json_data):
    author_list = []
    for author in json_data.get('author', ['']):
        given_name = author.get('given', '')
        family_name = author.get('family', '')
        author_list += [f'{given_name} {family_name}']
    return author_list


def extract_crossref_data(json_data):
    return {
        'publisher': json_data.get('publisher', ''),
        'page': json_data.get('page', ''),
        'year': json_data.get('created').get('date-parts')[0][0],
        'title': json_data.get('title', [''])[0],
        'authors': ', '.join(get_author_list(json_data)),
        'journal': json_data.get('container-title', [''])[0]
    }


def crossref_doi_lookup(doi):
    url = f'http://api.crossref.org/works/{doi}'
    json_data = url_to_json(url)
    if json_data is None:
        print(f'DOI: {doi} lookup failed')
        return None
    if 'message' in json_data.keys():
        return json_data['message']
    else:
        return None


# ----- Open Citations -----
def get_author_list(json_data):
    raw_author_list = json_data.get('author').split(';')
    author_list = []
    for raw_author in raw_author_list:
        x = raw_author.split(',')
        last_name = x[0]
        first_name = x[1]
        if len(x) == 3:
            orcid_id = x[2]
        author_list.append(f'{first_name} {last_name}'.strip())
    return author_list


def extract_opencitations_data(json_data):
    return {
        'authors': ', '.join(get_author_list(json_data)),
        'title': json_data.get('title'),
        'journal': json_data.get('source_title', ''),
        'volume': json_data.get('volume', ''),
        'issue': json_data.get('issue', ''),
        'page': json_data.get('page', ''),
        'year': json_data.get('year', ''),
        'citation_count': json_data.get('citation_count')
    }


def opencitations_doi_lookup(doi, version='v1'):
    url = f'https://opencitations.net/index/coci/api/{version}/metadata/{doi}'
    json_data = url_to_json(url)
    return json_data


def json_to_citation(json_data):
    citation_str = f"{json_data['authors']}, "
    citation_str += f"\"{json_data['title']}\" "
    citation_str += f"{json_data['journal']}"
    if json_data['volume'] != '':
        citation_str += ", {json_data['volume']}"
    if json_data['issue'] != '':
        citation_str += f"({json_data['issue']})"
    citation_str += f" {json_data['page']}"
    citation_str += f", {json_data['year']}."
    return citation_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('doi')
    args = parser.parse_args()
    doi = args.doi

    print(f'DOI: {doi}')

    results = opencitations_doi_lookup(doi)
    if len(results) > 0:
        for result in results:
            result2 = extract_opencitations_data(result)
            citation_str = json_to_citation(result2)
            print(citation_str)
