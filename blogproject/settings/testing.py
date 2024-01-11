from .base import *

DEBUG = False

ROOT_URLCONF = 'blogproject.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
