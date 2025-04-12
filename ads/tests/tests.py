import io
import os
import django
import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework import status
from django.urls import reverse
from ads.models import Ads
from rest_framework.test import APIClient


# Устанавливаем настройки для Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'swapsphere.settings'
django.setup()


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
@pytest.mark.django_db
def user():
    return User.objects.create_user(username='test_user', password='test')


@pytest.fixture
@pytest.mark.django_db
def ad(user):
    return Ads.objects.create(title="Test Ad", description="Test Description", user=user)

@pytest.mark.django_db
def test_ad_create(authenticated_client, user):
    client = authenticated_client
    url = 'http://127.0.0.1:8000/api/ads/create/'
    data = {
        'title': 'New Ad',
        'description': 'New Description',
        'category': 'test',
        'condition': 'new'
    }
    response = client.post(url, data, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_get_ad_list(authenticated_client, user):
    client = authenticated_client
    url = 'http://127.0.0.1:8000/api/ads/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    print(data)
    assert data['results'] == 2