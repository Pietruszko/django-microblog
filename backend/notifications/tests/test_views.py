import pytest
from django.urls import reverse
from notifications.models import Notification
from posts.models import Comment

@pytest.mark.django_db
def test_notification_viewset_list(authenticated_client):
    """Test reading own notifications."""
    url = reverse('notifications-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_notification_viewset_detail(authenticated_client, test_notification):
    """Test reading own single notification."""
    url = reverse('notifications-detail', args=[test_notification.id])
    response = authenticated_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_notification_viewset_detail_not_owner(second_client, test_notification):
    """Test not being able to read someones notification."""
    url = reverse('notifications-detail', args=[test_notification.id])
    response = second_client.get(url)
    assert response.status_code == 404 # 404 instead of 403 because it's not in their queryset

@pytest.mark.django_db
def test_marking_as_read_and_unread(authenticated_client, test_notification):
    """Test marking notifications as read and unread."""
    data = {"is_read": True}
    url = reverse('notifications-detail', args=[test_notification.id])
    response = authenticated_client.patch(url, data)
    assert response.status_code == 200
    test_notification.refresh_from_db()
    assert test_notification.is_read == True
    data2 = {"is_read": False}
    url = reverse('notifications-detail', args=[test_notification.id])
    response = authenticated_client.patch(url, data2)
    assert response.status_code == 200
    test_notification.refresh_from_db()
    assert test_notification.is_read == False

@pytest.mark.django_db
def test_marking_as_read_not_owner(second_client, test_notification):
    """Test marking notifications as read and unread."""
    data = {"is_read": True}
    url = reverse('notifications-detail', args=[test_notification.id])
    response = second_client.patch(url, data)
    assert response.status_code == 404

@pytest.mark.django_db
def test_marking_all_as_read(authenticated_client, test_user, second_user, test_post):
    """Testing custom mark_all_read view function."""
    for i in range(3):
        Comment.objects.create(
            user=second_user,
            post=test_post,
            content=f"Comment no.{i}",
        )
    assert Notification.objects.filter(recipient=test_user, is_read=False).count() == 3

    url = reverse('notifications-mark-all-read')
    response = authenticated_client.post(url)
    assert response.status_code == 200
    assert Notification.objects.filter(recipient=test_user, is_read=True).count() == 3

@pytest.mark.django_db
def test_deleting_all_notifications(authenticated_client, second_user, test_post, test_user):
    """Testing custom delete_all view function."""
    for i in range(3):
        Comment.objects.create(
            user=second_user,
            post=test_post,
            content=f"Comment no.{i}",
        )
    assert Notification.objects.filter(recipient=test_user).count() == 3

    url = reverse('notifications-delete-all')
    response = authenticated_client.delete(url)
    assert response.status_code == 204
    assert Notification.objects.filter(recipient=test_user).count() == 0

@pytest.mark.django_db
def test_deleting_single_notification(authenticated_client, test_notification):
    """Testing successful deleting of notification."""
    url = reverse('notifications-detail', args=[test_notification.id])
    response = authenticated_client.delete(url)
    assert response.status_code == 204

@pytest.mark.django_db
def test_deleting_single_notification_not_owner(second_client, test_notification):
    """Testing not successful deleting of someones notification."""
    url = reverse('notifications-detail', args=[test_notification.id])
    response = second_client.delete(url)
    assert response.status_code == 404
