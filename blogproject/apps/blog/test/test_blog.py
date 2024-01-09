from django.test import Client
import pytest


def test_home_view():
    client = Client()
    response = client.get('/blog/home/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_dashboard_view():
    client = Client()
    response = client.get('/blog/profile/')
    assert response.status_code == 200

