from django.urls import path
from .views import (
    CreatePostView,
    PostFeedView,
    LikePostView,
    AddCommentView,
    PostDetailView,
    CommentDetailView,
    CreateSittingRequestView,
)

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('feed/', PostFeedView.as_view(), name='post-feed'), # with search and filter options
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:post_id>/request/', CreateSittingRequestView.as_view(), name='create-sitting-request'),
]
