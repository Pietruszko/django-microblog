import pytest
from django.urls import reverse
from posts.models import Post

@pytest.mark.django_db
def test_post_filtering(authenticated_client, test_user, second_user):
    """Test DRF filtering."""
    Post.objects.bulk_create([
        Post(content=f"Post {i}", user=test_user) for i in range(3)
    ])
    Post.objects.bulk_create([
        Post(content=f"Test {i}", user=second_user) for i in range(2)
    ])

    url = reverse('posts-list')

    response = authenticated_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 5

    response = authenticated_client.get(f"{url}?user={second_user.id}")
    data = response.json()
    assert data['count'] == 2

    response = authenticated_client.get(f"{url}?search=Post")
    assert response.json()['count'] == 3

    first_post = Post.objects.order_by('-created_at').first()
    response = authenticated_client.get(f"{url}?ordering=-created_at")
    assert response.json()['results'][0]['id'] == first_post.id