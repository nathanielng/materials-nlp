# Coding Tools for Scientific Research

## 1. Background

This is a set of coding tools for scientific research.  There are currently two parts - a parsing and natural language processing engine 

### 1.1 Parsing & Natural Language Processing Engine and API Client

This is a parsing & Natural Language Processing (NLP) engine and API Client for scientific papers.
It will allow papers in PDF format to be parsed for their DOI's (digital object identifiers)
or their arXiv IDs.

Inn terms of API cliennts, for the time being, development will be prioritized towards the following

1. Elsevier API at [dev.elsevier.com/](http://dev.elsevier.com/)
2. [Crossref API](https://www.crossref.org/services/metadata-delivery/rest-api/) via [crossref_commons_py](https://gitlab.com/crossref/crossref_commons_py)

Tentative APIs currently under exploration:
1. [CORE](https://core.ac.uk/services/api/)
2. [Microsoft Academic Services](https://docs.microsoft.com/en-us/academic-services/)

For the NLP aspect, initial work will focus on on Materials Science,
via the [mat2vec](https://github.com/materialsintelligence/mat2vec) library
with a general direction to eventually cover at least the following 4 areas:

1. Materials Science
2. Engineering
3. Physics
4. Chemistry


## 2. Usage

### 2.1 Extracting a DOI from a file

```bash
python src/pdf_extract.py --file $FILE
```

### 2.2 Extracting multiple DOIs from a folder

```bash
python src/pdf_extract.py --path $FOLDER
```
