from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blogproject',
        'USER': 'postgres',
        'PASSWORD': 'psql',
        'HOST': 'db',
        'PORT': '5432',
    }
}
