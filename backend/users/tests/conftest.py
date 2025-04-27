import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(create_user):
    user = create_user(username='testuser', password='testpass123')
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client