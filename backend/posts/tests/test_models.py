import pytest
from ..models import Post
from django.contrib.auth.models import User
from django.db import IntegrityError
import datetime
from django.utils import timezone


@pytest.mark.django_db
def test_post_creation():
    """Test creation of new post."""
    user = User.objects.create_user(
        username='testuser', password='testpass123'
    )
    post = Post.objects.create(
        user = user,
        content = "This is my test post!",
    )
    assert post.user.username == 'testuser'
    assert post.created_at and post.content

@pytest.mark.django_db
def test_post_creation_invalid():
    """Test creating post with no user with expected fail."""
    with pytest.raises(IntegrityError):
        Post.objects.create(
        content = "This is my test post!",
    )
        
@pytest.mark.django_db
def test_post_creation_auto_created_at_field():
    """Test that 'created_at' is automatically set to current time."""
    user = User.objects.create_user(
        username='testuser', password='testpass123'
    )
    before_creation = timezone.now() # Time before creating post
    post = Post.objects.create(
        user = user,
        content = "This is my test post!",
    )
    after_creation = timezone.now() # Time after creating post

    assert post.created_at
    assert before_creation <= post.created_at <= after_creation
