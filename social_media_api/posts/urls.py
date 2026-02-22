from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, LikePostView, UnlikePostView

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]

urlpatterns += router.urls