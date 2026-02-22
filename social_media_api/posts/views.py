from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions,filters
from .models import Post, comment
from .serializers import PostSerializer, CommentSerializer

class IsOwnerorReadOnly(permissions.BasePermission):
    """
     custom permission to allow only owners of an object to edit it or delete it

    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerorReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerorReadOnly]
     
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


       
 