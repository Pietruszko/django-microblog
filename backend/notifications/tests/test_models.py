import pytest
from notifications.models import Notification

@pytest.mark.django_db
def test_notification_creation(test_user, test_post, second_user, test_comment):
    """Test that model works correctly."""
    notification = Notification.objects.create(
        recipient = test_user,
        sender = second_user,
        post = test_post,
        comment = test_comment,
        message = "Notification message",
    )
    assert notification.recipient == test_user
    assert notification.sender == second_user
    assert notification.post == test_post
    assert notification.comment == test_comment
    assert notification.message == "Notification message"
    assert notification.is_read == False
    assert notification.created_at is not None