import pytest
from ..models import UserProfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_user_profile_creation():
    """Test creation of User profile."""
    user = User.objects.create_user(
        username='testuser', password='testpass123'
    )
    avatar = SimpleUploadedFile(
        name='test_avatar.jpg', content=b'', content_type='image/jpeg'
    )
    profile = UserProfile.objects.create(
        user = user,
        first_name='John',
        last_name='Doe',
        bio='Test bio',
        avatar=avatar,
    )

    assert profile.user.username == 'testuser'
    assert profile.first_name == 'John'
    assert profile.bio == 'Test bio'
    assert profile.avatar.name.startswith('avatars/')

@pytest.mark.django_db
def test_user_profile_creation_default_bio():
    """Test creation of User profile with default bio and no avatar."""
    user = User.objects.create_user(
        username='testuser', password='testpass123'
    )
    profile = UserProfile.objects.create(
        user = user,
        first_name='John',
        last_name='Doe',
    )

    assert profile.user.username == 'testuser'
    assert profile.first_name == 'John'
    assert profile.bio == 'This is my profile!'
    assert profile.avatar == None
