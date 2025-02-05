from django.urls import path
from .views import (
    CreatePostView,
    PostFeedView,
    LikePostView,
    AddCommentView,
    PostDetailView,
    CommentDetailView,
    CreateSittingRequestView,
    SentSittingRequestsView,
    IncomingSittingRequestsView,
    ManageSittingRequestView,
)

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('feed/', PostFeedView.as_view(), name='post-feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:post_id>/request/', CreateSittingRequestView.as_view(), name='create-sitting-request'),
    path('requests/sent/', SentSittingRequestsView.as_view(), name='sent-sitting-requests'),
    path('requests/incoming/', IncomingSittingRequestsView.as_view(), name='incoming-sitting-requests'),
    path('requests/manage/<int:request_id>/', ManageSittingRequestView.as_view(), name='manage-sitting-request'),
]
