import pytest
from ..serializers import RegisterSerializer
from ..models import UserProfile

@pytest.mark.django_db
def test_register_serializer_create_valid_data():
    """Test register serializer creates valid user"""
    data = {
        "username": "testuser",
        "password": "testpass123",
        "first_name": "John",
        "last_name": "Doe",
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.userprofile.first_name == data['first_name']
    assert UserProfile.objects.count() == 1

@pytest.mark.django_db
def test_register_serializer_password_write_only():
    data = {
        "username": "testuser",
        "password": "testpass123",
        "first_name": "John",
        "last_name": "Doe",
    }
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    serializer.save()
    assert 'password' not in serializer.data

@pytest.mark.django_db
def test_register_serializer_create_invalid_data():
    """Test register serializer with invalid data"""
    data = {
        "password": "testpass123",
        "last_name": "Doe",
    }
    serializer = RegisterSerializer(data=data)
    assert not serializer.is_valid()
    assert 'username' in serializer.errors
    assert 'first_name' in serializer.errors