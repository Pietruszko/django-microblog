import pytest
from notifications.serializers import NotificationSerializer
from notifications.serializers import Notification

@pytest.mark.django_db
def test_notification_serializer_create_valid_data(test_notification):
    """Test notification serializer creates valid notification."""
    serializer = NotificationSerializer(test_notification)
    data = serializer.data
    assert "commented on your post" in data['message']
    assert set(data.keys()) == {
        'id', 'message', 'is_read', 'created_at',
        'post_id', 'comment_id', # added by to_representation
    }
    assert data['post_id'] == test_notification.post_id
    assert data['comment_id'] == test_notification.comment_id

@pytest.mark.django_db
def test_notification_serializer_validation(test_notification):
    """Test is_read field validation."""
    # valid update
    serializer = NotificationSerializer(
        instance=test_notification,
        data={'is_read': True},
        partial=True
    )
    assert serializer.is_valid(), serializer.errors
    
    # try to modify read-only field
    data={'message': 'Hacked!'}
    serializer = NotificationSerializer(
        instance=test_notification,
        data=data,
        partial=True
    )
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.message != data['message']
    assert "commented on your post" in updated.message

