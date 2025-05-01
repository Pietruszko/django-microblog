import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from posts.models import Post, Comment
from notifications.models import Notification

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

@pytest.fixture
def second_user():
    return User.objects.create_user(
        username="testuser2", password="testpass1234"
    )

@pytest.fixture
def second_client(second_user):
    refresh = RefreshToken.for_user(second_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.fixture
def test_comment(second_user, test_post):
    return Comment.objects.create(
        content="Test comment",
        user=second_user,
        post=test_post,
    )

@pytest.fixture
def test_notification(test_user, second_user, test_post, test_comment):
    return Notification.objects.create(
        recipient=test_user,
        sender=second_user,
        post=test_post,
        comment=test_comment,
        message=f"{second_user.username} commented on your post"
    )
