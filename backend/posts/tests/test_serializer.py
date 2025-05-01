import pytest
from ..serializers import PostSerializer, CommentSerializer
from ..models import Post, Comment
from rest_framework.test import APIRequestFactory

@pytest.mark.django_db
def test_post_serializer_create_valid_data(test_user):
    """Test post serializer creates valid post."""
    factory = APIRequestFactory()
    request = factory.post("/test-url/")
    request.user = test_user

    data = {
        "content": "Post about testing serializer",
    }
    serializer = PostSerializer(
        data=data, context={'request': request}
    )
    assert serializer.is_valid(), serializer.errors
    post = serializer.save()
    assert post.content == data["content"]
    assert post.user == test_user
    assert Post.objects.count() == 1

@pytest.mark.django_db
def test_comment_serializer_create_valid_data(test_user, test_post):
    """Test comment serializer creates valid comment."""
    factory = APIRequestFactory()
    request = factory.post("/test-url/")
    request.user = test_user

    data = {
        "content": "Comment testing serializer",
    }
    serializer = CommentSerializer(
        data=data, context={'request': request}
    )
    assert serializer.is_valid(), serializer.errors
    comment = serializer.save(post=test_post)
    assert comment.content == data["content"]
    assert comment.user == test_user
    assert Comment.objects.count() == 1