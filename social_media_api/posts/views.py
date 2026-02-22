from rest_framework import viewsets, permissions,status, generics
from rest_framework.views import APIView
from .models import Post, Comment ,Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from notifications.models import Notification

class IsOwnerorReadOnly(permissions.BasePermission):
    """
     custom permission to allow only owners of an object to edit it or delete it

    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    
""" 
    
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


    @action(detail=True, methods=['post'])
    def like(self,request,pk=None):
        post=self.get.object()
        user=request.user

        Like,created=Like.objects.get_or_create(user=user,post=post)

        if not created:
            return Response({'status':'already liked'}, status=400)
        
        if post.author !=user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target=post
            )
        return Response({'status':'post liked'}, status=201)
    

    @action(detail=True, methods=['post'])
    def unlike(self,request,pk=None):
        post=self.get-object()
        user=request.user

        try:
            like=Like.objects.get(user=user,post=post)
            like.delete()
            return Response({'status':'post unliked'}, status=200)
        except Like.DoesNotExist:
            return Response({'status':'not liked yet'}, status=400)
""" 

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        Like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response(
            {"detail": "Post liked successfully."},
            status=status.HTTP_201_CREATED
        )


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked successfully."})
        except Like.DoesNotExist:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerorReadOnly]
     
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    
 