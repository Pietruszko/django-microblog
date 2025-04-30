from .models import Post
from .serializers import PostSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """Custom Permission to only allow owners edit/delete objects."""
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return obj.user == request.user
        

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all() # Default queryset (required for router)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return super().get_queryset()
