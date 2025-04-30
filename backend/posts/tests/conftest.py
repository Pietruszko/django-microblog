import pytest
from django.contrib.auth.models import User

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser", password="testpass123"
    )