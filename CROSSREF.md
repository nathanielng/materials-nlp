# Crossref REST APIs

## 1. Introduction

The Crossref REST APIs provide various academic query services,
including a means to retrieve journal information from dois.

The documentation is available at https://github.com/CrossRef/rest-api-doc


## 2. Software & Libraries to access the Crossref REST APIs

### 2.1 REST APIs

- `curl`
- `httpie`

### 2.2 Available Python libraries

- [crossref-commons](https://gitlab.com/crossref/crossref_commons_py)
- [habanero](https://github.com/sckott/habanero)
- [crossrefapi](https://github.com/fabiobatalha/crossrefapi)


## 3. Usage

### 3.1 httpie

Install `httpie` using `pip install httpie`.
Next, retrieve data from any DOI using the following

```bash
http http://api.crossref.org/works/{INSERT_DOI_HERE}
```
