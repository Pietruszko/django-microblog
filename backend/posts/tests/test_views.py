import pytest
from django.urls import reverse
from ..models import Post

@pytest.mark.django_db
def test_post_viewset(authenticated_client, test_user):
    """Test post view creating new post."""
    data = {
        "content": "Post about testing serializer",
    }
    url = reverse('posts-list')
    response = authenticated_client.post(url, data)
    assert response.status_code == 201
    assert response.data['content'] == data['content']
    assert Post.objects.count() == 1
    assert Post.objects.first().user == test_user

@pytest.mark.django_db
def test_post_read_unauthorized(unauthenticated_client, test_post):
    """Test that unauthorized users can read others posts (like in blog)."""
    url = reverse('posts-detail', args=[test_post.id])
    response = unauthenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_editing_post_content(authenticated_client, test_post):
    """Test editing posts by authorized users."""
    data = {
        "content": "This is changed content",
    }
    url = reverse('posts-detail', args=[test_post.id])
    response = authenticated_client.put(url, data)
    assert response.status_code == 200
    test_post.refresh_from_db()
    assert test_post.content == data['content']



