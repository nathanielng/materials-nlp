# Coding Tools for Scientific Research

## 1. Background

This is a set of coding tools for scientific research.  The intention is to have at least three parts:

1. an article lookup / API client
2. a parsing and natural language processing engine
3. a bot linking to Twitter feeds and Discord

### 1.1 Article Lookup / API Client

Article lookup will be carried out using an API Client for scientific papers.
Initially, development will be prioritized towards the following

1. Open Citations API at [opencitations.net](http://opencitations.net/index/coci/api/v1)
2. [Crossref API](https://www.crossref.org/services/metadata-delivery/rest-api/) via [crossref_commons_py](https://gitlab.com/crossref/crossref_commons_py)

Tentative APIs currently under exploration:
1. Elsevier API at [dev.elsevier.com/](http://dev.elsevier.com/)
2. [CORE](https://core.ac.uk/services/api/)
3. [Microsoft Academic Services](https://docs.microsoft.com/en-us/academic-services/)

### 1.2 Parsing & Natural Language Processing Engine

For the NLP aspect, initial work will focus on on Materials Science,
via the [mat2vec](https://github.com/materialsintelligence/mat2vec) library
with a general direction to eventually cover at least the following 4 areas:

1. Materials Science
2. Engineering
3. Physics
4. Chemistry

For a start, the initial tool is `pdf_extract.py` which extracts the text of a `pdf` file.
The text is parsed for DOI (digital object identifier) data and arXiv IDs.
At a later stage, the text may be used as an input to the parsing & Natural Language Processing (NLP) engine.


## 2. Usage

### 2.1 Parser

#### 2.1.1 Extracting a DOI from a file

```bash
python src/pdf_extract.py --file $FILE
```

#### 2.1.2 Extracting multiple DOIs from a folder

```bash
python src/pdf_extract.py --path $FOLDER
```

### 2.2 Discord Bot

A bot based on some of the tools here will eventually be made available for testing at the following Discord: https://discord.gg/ZPnKCkU 
