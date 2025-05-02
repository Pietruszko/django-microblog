import pytest
from django.urls import reverse
from posts.models import Post

@pytest.mark.django_db
def test_post_pagination(authenticated_client, test_user):
    """Test pagination (basic DRF pagination with 10 objects per page)."""
    Post.objects.bulk_create([
        Post(content=f"Post {i}", user=test_user) for i in range (15)
    ])

    url = reverse('posts-list')
    response = authenticated_client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert 'results' in data
    assert data['count'] == 15
    assert len(data['results']) == 10
    assert data['next'] is not None
    assert data['next'].endswith('2')
    assert data['previous'] is None

    response_page_2 = authenticated_client.get(data['next'])
    data_page_2 = response_page_2.json()
    assert response_page_2.status_code == 200
    assert len(data_page_2['results']) == 5
    assert data_page_2['next'] is None
    assert data_page_2['previous'] is not None
    assert data_page_2['previous'].endswith(url)