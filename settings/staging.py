from .base import *

DEBUG = True

ALLOWED_HOSTS = ["fs-api-staging-32ygwzcnka-ue.a.run.app"]

SITE_URL = 'https://staging-front-street-ug.web.app/'

# STAGING
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.getenv('DATABASE_NAME_STAGING'),
        'USER': os.getenv('DATABASE_USER_STAGING'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD_STAGING'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", "use_pure": True},
    }
}
