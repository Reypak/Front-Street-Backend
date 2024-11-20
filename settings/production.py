from .base import *

DEBUG = False

ALLOWED_HOSTS = ["fs-api-32ygwzcnka-ue.a.run.app"]

SITE_URL = 'https://front-street-ug.web.app/'

# PRODUCTION
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", "use_pure": True},
    }
}
