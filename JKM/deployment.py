import os
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'], 
                 'webapp.jkmevents.in',
                 "www.jkmevents.in",
                 "https://www.jkmevents.in"]

CSRF_TRUSTED_ORIGINS = ["https://"+ os.environ['WEBSITE_HOSTNAME'], 
                        'webapp.jkmevents.in',
                        "www.jkmevents.in",
                        "https://www.jkmevents.in"]

DEBUG = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jkm-database',
        'USER': 'tnriqkkrsy',
        'PASSWORD': 'FL44SH21B7S87LHR$',
        'HOST': 'jkm-server.mysql.database.azure.com',
        'PORT': '3306',
    }

}


