import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_create():
    client = APIClient()
    url = reverse('user-create')
    response = client.post(url, {'username': 'test_user', 'password': 'test_password123'}, format='json')
    assert response.status_code == 201
    assert User.objects.filter(username='test_user').exists()

