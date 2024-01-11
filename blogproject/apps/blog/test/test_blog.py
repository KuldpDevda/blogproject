from django.test import Client
import pytest
from django.test import TestCase

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

