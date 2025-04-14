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
def user1():
    return User.objects.create_user(username='test_user', password='test')
@pytest.fixture
@pytest.mark.django_db
def user2():
    return User.objects.create_user(username='test_user2', password='test_2')

@pytest.fixture
@pytest.mark.django_db
def ad(user):
    return Ads.objects.create(title="Test Ad", description="Test Description", user=user)

@pytest.fixture
@pytest.mark.django_db
def client1(user1):
    client = APIClient()
    client.force_authenticate(user=user1)
    return client


@pytest.fixture
@pytest.mark.django_db
def client2(user2):
    client = APIClient()
    client.force_authenticate(user=user2)
    return client



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
    test_ad_create(authenticated_client, user)
    client = authenticated_client
    url = 'http://127.0.0.1:8000/api/ads/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    print(data['results'])
    assert len(data['results']) == 1


@pytest.mark.django_db
def test_delete_ad(authenticated_client, user):
    client = authenticated_client
    test_ad_create(authenticated_client, user)
    url = 'http://127.0.0.1:8000/api/ads/1/'
    response = client.delete(url)
    print(response.data['message'])
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data['message'] == 'Success deleted'

@pytest.mark.django_db
def test_update_ad(authenticated_client, user):
    client = authenticated_client
    test_ad_create(authenticated_client, user)
    url = 'http://127.0.0.1:8000/api/ads/1/'
    data = {
        'title': 'New Ad',
        'description': 'New Description UPDATE',
        'category': 'test',
        'condition': 'new'
    }
    response = client.put(url, data, format='multipart')
    assert response.data['message'] == "Ad updated successfully"



@pytest.mark.django_db
def test_exchange_flow(client1, client2, user1, user2):
    response1 = client1.post('/api/ads/create/', {
        "title": "Phone",
        "description": "Samsung",
        "category": "Electronics",
        "condition": "used",
    }, format='json')
    assert response1.status_code == status.HTTP_201_CREATED
    ad1_id = response1.data['id']

    response2 = client2.post('/api/ads/create/', {
        "title": "Laptop",
        "description": "Asus ROG",
        "category": "PC",
        "condition": "new",
    }, format='json')
    assert response2.status_code == status.HTTP_201_CREATED
    ad2_id = response2.data['id']

    exchange_response = client1.post('/api/exchange/create/', {
        "ad_sender": ad1_id,
        "ad_receiver": ad2_id,
        "comment": "asd"
    }, format='json')
    print(exchange_response.data)
    assert exchange_response.status_code == status.HTTP_201_CREATED

    exchange_id = exchange_response.data['id']

    confirm_response = client2.get(f'/api/exchange/confirm/{exchange_id}/confirm_exchange/', format='json')
    print(confirm_response.data)
    assert confirm_response.status_code == status.HTTP_200_OK
    assert confirm_response.data['status'] == 'confirmed'
