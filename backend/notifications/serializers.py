from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'message': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['post_id'] = instance.post_id
        data['comment_id'] = instance.comment_id
        return data
