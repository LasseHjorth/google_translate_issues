from dotenv import load_dotenv
import os
from google.cloud import translate_v3 as translate
from google.api_core.client_options import ClientOptions
from uuid import uuid4
from google.cloud import storage

load_dotenv()


# This scripts tries to create a glossary in global using global endpoint.
#
#

GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
GOOGLE_STORAGE_BUCKET = os.getenv("GOOGLE_STORAGE_BUCKET")


# choose location
location = "europe-west1"
api_endpoint = "translate-eu.googleapis.com"

# Set variables

source_lang_code = "en"
target_lang_codes = "da"
timeout = 60 
uuid = uuid4()
input_uri = f"gs://{GOOGLE_STORAGE_BUCKET}/{uuid}.docx"

# clients
client = translate.TranslationServiceClient(client_options=ClientOptions(api_endpoint=api_endpoint))
storage_client = storage.Client()

# Upload a document for translating.
bucket = storage_client.bucket(GOOGLE_STORAGE_BUCKET)
blob = bucket.blob(f"{uuid}.docx")
blob.upload_from_filename("resources/document.docx")


# Translate document
parent = f"projects/{GOOGLE_PROJECT_ID}/locations/{location}"

input_config = translate.DocumentInputConfig()
input_config.gcs_source.input_uri = input_uri

#glossary = ""
glossary_config = None
# glossary_parsed = client.parse_glossary_path(glossary)
# glossary_path = client.glossary_path(glossary_parsed['project'],glossary_parsed['location'],glossary_parsed['glossary'])
# glossary_config = translate.TranslateTextGlossaryConfig(glossary=glossary_path)

request = translate.TranslateDocumentRequest(
    parent=parent,
    source_language_code=source_lang_code,
    target_language_code=target_lang_codes,
    document_input_config=input_config,
    glossary_config=glossary_config,
)

# Make the request
response = client.translate_document(request=request)
print(response)