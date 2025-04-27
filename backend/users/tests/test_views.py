import pytest
from django.urls import reverse
from ..models import UserProfile

@pytest.mark.django_db
def test_register_view(client):
    """Test register view creating new user"""
    data = {
        "username": "testuser",
        "password": "testpass123",
        "first_name": "John",
        "last_name": "Doe",
    }
    response = client.post(reverse('register'), data)
    assert response.status_code == 201
    assert response.data['username'] == data['username']
    assert UserProfile.objects.count() == 1