from django.urls import path
from .views import CreatePostView
from .views import PostFeedView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-post'),
    path('feed/', PostFeedView.as_view(), name='post-feed'),
]
