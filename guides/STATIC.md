# Google Cloud Storage

## Create Bucket

## Create Service Account

## Create Key

Download json file and place in project root directory

## Install dependencies

` pip install django-storages[google]`

Then run

`pip freeze > requirements.txt`

## Add Configurations

In the `settings.py` file.

### Import Credentials

```bash
from google.oauth2 import service_account
# service account file
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    'credentials.json')
```

Then:

```bash
# CLOUD STORAGE
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

# Google Cloud Storage for Static File Serve
GS_PROJECT_ID = 'front-street-ug'
GS_BUCKET_NAME = 'front-street-ug'

GS_AUTO_CREATE_BUCKET = True
GS_DEFAULT_ACL = 'publicRead'

STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
```

## Collect static files

`python manage.py collectstatic`

## Deploy to Cloud Run
