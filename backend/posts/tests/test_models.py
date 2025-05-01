import pytest
from ..models import Post, Comment
from django.db import IntegrityError
from django.utils import timezone


@pytest.mark.django_db
def test_post_creation(test_user):
    """Test creation of new post."""
    post = Post.objects.create(
        user = test_user,
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
def test_post_creation_auto_created_at_field(test_user):
    """Test that 'created_at' is automatically set to current time."""
    before_creation = timezone.now() # Time before creating post
    post = Post.objects.create(
        user = test_user,
        content = "This is my test post!",
    )
    after_creation = timezone.now() # Time after creating post

    assert post.created_at
    assert before_creation <= post.created_at <= after_creation

@pytest.mark.django_db
def test_comment_model_creates_successfully(test_post, test_user):
    """Test that a Comment instance is created with valid data."""
    comment = Comment.objects.create(
        user = test_user,
        post = test_post,
        content = "Nice post!",
    )

    assert comment.user == test_user
    assert comment.post == test_post
    assert comment.content == "Nice post!"
    assert comment.created_at is not None
    assert Comment.objects.count() == 1
