from rest_framework.viewsets import ModelViewSet
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class IsNotificationOwner(BasePermission):
    """Custom permission."""
    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated, IsNotificationOwner]
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']

    def get_queryset(self):
        return self.request.user.notifications.select_related(
            'sender', 'post', 'comment'
        )
    
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return Response(status=200)
    
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        request.user.notifications.all().delete()
        return Response(status=204)

