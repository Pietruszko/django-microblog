import pytest
from django.urls import reverse
from ..models import Post, Comment

@pytest.mark.django_db
class TestPostViewSet:
    def test_post_viewset(self, authenticated_client, test_user):
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

    def test_post_read_unauthorized(self, unauthenticated_client, test_post):
        """Test that unauthorized users can read others posts (like in blog)."""
        url = reverse('posts-detail', args=[test_post.id])
        response = unauthenticated_client.get(url)
        assert response.status_code == 200

    def test_editing_post_content(self, authenticated_client, test_post):
        """Test editing posts by authorized users."""
        data = {
            "content": "This is changed content",
        }
        url = reverse('posts-detail', args=[test_post.id])
        response = authenticated_client.put(url, data)
        assert response.status_code == 200
        test_post.refresh_from_db()
        assert test_post.content == data['content']

    def test_deleting_post(self, authenticated_client, test_post):
        """Test deleting posts by authorized users."""
        url = reverse('posts-detail', args=[test_post.id])
        response = authenticated_client.delete(url)
        assert response.status_code == 204

    def test_editing_post_content_unauthorized(self, unauthenticated_client, test_post):
        """Test editing posts by unauthorized users."""
        data = {
            "content": "This is changed content",
        }
        url = reverse('posts-detail', args=[test_post.id])
        response = unauthenticated_client.put(url, data)
        assert response.status_code == 401
        test_post.refresh_from_db()
        assert test_post.content != data['content']

    def test_deleting_post_unauthorized(self, unauthenticated_client, test_post):
        """Test deleting posts by unauthorized users."""
        url = reverse('posts-detail', args=[test_post.id])
        response = unauthenticated_client.delete(url)
        assert response.status_code == 401

    def test_editing_post_content_not_author(self, test_post, second_client):
        """Test editing posts not by author (should fail with 403)."""
        data = {
            "content": "This is hacked content",
        }
        url = reverse('posts-detail', args=[test_post.id])
        response = second_client.put(url, data)
        assert response.status_code == 403
        test_post.refresh_from_db()
        assert test_post.content != data['content']

    def test_deleting_post_not_author(self, test_post, second_client):
        """Test deleting posts not by author (should fail with 403)."""
        url = reverse('posts-detail', args=[test_post.id])
        response = second_client.delete(url)
        assert response.status_code == 403

@pytest.mark.django_db
class TestCommentViewSet:
    def test_comment_viewset(self, authenticated_client, test_post):
        """Test comment view creating new comment."""
        data = {
            "content": "Comment testing serializer",
        }
        url = reverse('post-comments-list', kwargs={'post_pk': test_post.id})
        response = authenticated_client.post(url, data)
        assert response.status_code == 201
        assert response.data['content'] == data['content']
        assert Comment.objects.count() == 1
        assert test_post.comments.count() == 1

    def test_comment_read_all_unauthorized(self, unauthenticated_client, test_post):
        """Test that unauthorized users can read all comments under a post."""
        url = reverse('post-comments-list', kwargs={'post_pk': test_post.id})
        response = unauthenticated_client.get(url)
        assert response.status_code == 200

    def test_comment_read_single_unauthorized(self, unauthenticated_client, test_post, test_comment):
        """Test that unauthorized users can read single comment under a post."""
        url = reverse('post-comments-detail', kwargs={
            'post_pk': test_post.id,
            'pk': test_comment.id,
        })
        response = unauthenticated_client.get(url)
        assert response.status_code == 200
        assert response.data['content'] == test_comment.content

    def test_editing_comment_content(self, authenticated_client, test_post, test_comment):
        """Test editing comments by authorized users."""
        data = {
            "content": "This is changed comment",
        }
        url = reverse('post-comments-detail', kwargs={
            'post_pk': test_post.id,
            'pk': test_comment.id,
        })
        response = authenticated_client.put(url, data)
        assert response.status_code == 200
        test_comment.refresh_from_db()
        assert test_comment.content == data['content']

    def test_deleting_comment(self, authenticated_client, test_post, test_comment):
        """Test deleting comments by authorized users."""
        url = reverse('post-comments-detail', kwargs={
            'post_pk': test_post.id,
            'pk': test_comment.id,
        })
        response = authenticated_client.delete(url)
        assert response.status_code == 204

    def test_editing_comment_content_unauthorized(self, unauthenticated_client, test_post, test_comment):
        """Test editing comments by unauthorized users."""
        data = {
            "content": "This is changed comment",
        }
        url = reverse('post-comments-detail', kwargs={
            'post_pk': test_post.id,
            'pk': test_comment.id,
        })
        response = unauthenticated_client.put(url, data)
        assert response.status_code == 401
        test_comment.refresh_from_db()
        assert test_comment.content != data['content']

    def test_deleting_comment_unauthorized(self, unauthenticated_client, test_post, test_comment):
        """Test deleting comments by unauthorized users."""
        url = reverse('post-comments-detail', kwargs={
            'post_pk': test_post.id,
            'pk': test_comment.id,
        })
        response = unauthenticated_client.delete(url)
        assert response.status_code == 401

    def test_editing_comment_content_not_author(self, test_post, second_client, test_comment):
        """Test editing comments not by author (should fail with 403)."""
        data = {
            "content": "This is hacked comment",
        }
        url = reverse('post-comments-detail', kwargs={
            'post_pk': test_post.id,
            'pk': test_comment.id,
        })
        response = second_client.put(url, data)
        assert response.status_code == 403
        test_comment.refresh_from_db()
        assert test_comment.content != data['content']

    def test_deleting_comment_not_author(self, test_post, second_client, test_comment):
        """Test deleting comments not by author (should fail with 403)."""
        url = reverse('post-comments-detail', kwargs={
            'post_pk': test_post.id,
            'pk': test_comment.id,
        })
        response = second_client.delete(url)
        assert response.status_code == 403