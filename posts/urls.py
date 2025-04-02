from django.urls import path
from likes.views import PostLikeAPIView
from .views import (
    CreatePostView,
    PostFeedView,
    LikePostView,
    AddCommentView,
    PostDetailView,
    CommentDetailView,
    ListCommentsView,
    CreateSittingRequestView,
    SentSittingRequestsView,
    IncomingSittingRequestsView,
    ManageSittingRequestView,
    AllPosts,
)

urlpatterns = [
    path('', CreatePostView.as_view(), name='create-post'),
    path('all/', AllPosts.as_view(), name='all-posts'),
    path('feed/', PostFeedView.as_view(), name='post-feed'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/comments/', ListCommentsView.as_view(), name='list-comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:post_id>/request/', CreateSittingRequestView.as_view(), name='create-sitting-request'),
    path('requests/sent/', SentSittingRequestsView.as_view(), name='sent-sitting-requests'),
    path('requests/incoming/', IncomingSittingRequestsView.as_view(), name='incoming-sitting-requests'),
    path('requests/manage/<int:request_id>/', ManageSittingRequestView.as_view(), name='manage-sitting-request'),
    path('<int:post_id>/like/', PostLikeAPIView.as_view(), name='post-like'),
]
