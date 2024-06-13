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

api_endpoint = "translate.googleapis.com"
location = "us-central1"

# Set variables
source_lang_code = "en"
target_lang_codes = ["da","sv"]
timeout = 60 
uuid = uuid4()
input_uri = f"gs://{GOOGLE_STORAGE_BUCKET}/{uuid}.csv"

# clients

client = translate.TranslationServiceClient(client_options=ClientOptions(api_endpoint=api_endpoint))
storage_client = storage.Client()



# Upload a glossary for importing.
bucket = storage_client.bucket(GOOGLE_STORAGE_BUCKET)
blob = bucket.blob(f"{uuid}.csv")
blob.upload_from_filename("resources/glossary.csv")


# Create a glossary - in the location specified above.

name = client.glossary_path(GOOGLE_PROJECT_ID, location, f"glosssary_{uuid}")
language_codes_set = translate.types.Glossary.LanguageCodesSet(
    language_codes=[source_lang_code] + target_lang_codes
)

gcs_source = translate.types.GcsSource(input_uri=input_uri)

input_config = translate.types.GlossaryInputConfig(gcs_source=gcs_source)

glossary = translate.types.Glossary(
    name=name, language_codes_set=language_codes_set, input_config=input_config,display_name=f"{uuid}"
)

parent = f"projects/{GOOGLE_PROJECT_ID}/locations/{location}"

print(glossary)

operation = client.create_glossary(parent=parent, glossary=glossary)

result = operation.result(timeout)
print(f"Created: {result.name}")
print(f"Input Uri: {result.input_config.gcs_source.input_uri}")

# Fetch the glossary created

response = client.get_glossary(name=name)
print(response)
print(f"Glossary name: {response.name}")
print(f"Entry count: {response.entry_count}")
print(f"Input URI: {response.input_config.gcs_source.input_uri}")



