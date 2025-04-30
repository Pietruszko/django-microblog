import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Post

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser", password="testpass123"
    )

@pytest.fixture
def authenticated_client(test_user):
    refresh = RefreshToken.for_user(test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.fixture
def test_post(test_user):
    return Post.objects.create(
        content="Testing content",
        user=test_user
    )

@pytest.fixture
def unauthenticated_client():
    return APIClient()
