import pytest
from ..serializers import PostSerializer
from ..models import Post
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