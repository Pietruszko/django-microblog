import pytest
from posts.models import Comment, Post
from notifications.models import Notification
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_notification_on_comment(test_user, second_user, test_post):
    """Test that signals work and create notification on comment."""
    comment = Comment.objects.create(
        user = second_user,
        post = test_post,
        content = "Nice post!"
    )

    assert Notification.objects.count() == 1
    notification = Notification.objects.first()
    assert notification is not None
    assert notification.recipient == test_user
    assert notification.sender == second_user
    assert notification.comment == comment
    assert notification.message.startswith(f"{second_user.username} commented:")


@pytest.mark.django_db
def test_not_create_notification_on_self_comment(test_user, test_post):
    """Test that there is no notification when commenting own post."""
    comment = Comment.objects.create(
        user = test_user,
        post = test_post,
        content = "Nice post!"
    ) 

    assert Notification.objects.first() is None