from django.urls import path
from likes.views import PostLikeAPIView
from rest_framework.routers import DefaultRouter
from posts.views_messages import SittingResponseMessageViewSet
from .views import (
    AuthorPostsList,
    CreatePostView,
    PostFeedView,
    LikePostView,
    PostDetailView,
    CreateSittingRequestView,
    SittingRequestDetailView,
    SentSittingRequestsView,
    IncomingSittingRequestsView,
    ManageSittingRequestView,
    AllPosts,
)

router = DefaultRouter()
router.register(r"sitting-messages", SittingResponseMessageViewSet, basename="sitting-messages")

urlpatterns = [
    path('', CreatePostView.as_view(), name='create-post'),
    path('author-posts/', AuthorPostsList.as_view(), name="author-posts"),
    path('all/', AllPosts.as_view(), name='all-posts'),
    path('feed/', PostFeedView.as_view(), name='post-feed'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/request/', CreateSittingRequestView.as_view(), name='create-sitting-request'),
    path("requests/<int:pk>/", SittingRequestDetailView.as_view(), name="sitting-request-detail"),
    path('requests/sent/', SentSittingRequestsView.as_view(), name='sent-sitting-requests'),
    path('requests/incoming/', IncomingSittingRequestsView.as_view(), name='incoming-sitting-requests'),
    path('requests/manage/<int:request_id>/', ManageSittingRequestView.as_view(), name='manage-sitting-request'),
    path('<int:post_id>/like/', PostLikeAPIView.as_view(), name='post-like'),
]

urlpatterns += router.urls
