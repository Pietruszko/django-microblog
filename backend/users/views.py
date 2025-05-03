from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.select_related('user')
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'