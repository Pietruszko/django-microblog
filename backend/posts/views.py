from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
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
    
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all() # Default queryset (required for router)
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(user=self.request.user, post_id=post_id)
