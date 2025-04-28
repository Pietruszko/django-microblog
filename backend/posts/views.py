from .models import Post
from .serializers import PostSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all() # Default queryset (required for router)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return super().get_queryset()
