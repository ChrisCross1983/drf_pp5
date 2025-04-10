from django.urls import path
from .views import CommentList, CommentDetail, ToggleCommentLike

urlpatterns = [
    path('', CommentList.as_view(), name="comments-list"),
    path('<int:pk>/like/', ToggleCommentLike.as_view(), name='comment-like'),
    path('<int:pk>/', CommentDetail.as_view(), name="comments-detail")
]
