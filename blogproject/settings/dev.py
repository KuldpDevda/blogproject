from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blogproject',
        'USER': 'postgres1',
        'PASSWORD': 'psql',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}