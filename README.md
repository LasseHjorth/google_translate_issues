# Issues for google translation api.


## Initialize venv
```
python3.10 -m venv venv
source venv/bin/activate
(venv) pip install -r requirements.txt
```

## environment variables
GOOGLE_PROJECT_ID - the name of the project.

GOOGLE_STORAGE_BUCKET - the name of the bucket to use.


## create_glossary.py

- Uploads resources/glossary.csv to GOOGLE_STORAGE_BUCKET
- Creates a glossary in the location defined on line 23.
- Fetches the glossary created.



## Issues

1. Not possible to create a glossary in "global" - only in us-central1. Doesn't matter where the bucket is located.  (us,eu,europe-west1, us-central1).
2. To create a glossary in eu, europe-west1 is needed and api_endpoint should be translate-eu.googleapis.com.
3. To translate a document - global endpoint is needed, not supported by regional endpoints. Glossary can only be in us-central1 as a consquence, documents are processed in US.
