from django.test import Client
import pytest
from django.test import TestCase
import sys
import os

sys.path.append(os.path.abspath('/home/dell/Project/blogproject'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'blogproject.settings.dev'

import django
django.setup()



@pytest.mark.django_db
def test_home_view():
    client = Client()
    response = client.get('')
    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_view():
    client = Client()
    response = client.get('/signup/')
    assert response.status_code == 200

