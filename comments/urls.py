from django.urls import path
from comments import views
from .views import ToggleCommentLike

urlpatterns = [
    path('', views.CommentList.as_view(), name="comments-list"),
    path('comments/<int:pk>/like/', ToggleCommentLike.as_view(), name='comment-like'),
    path('<int:pk>/', views.CommentDetail.as_view(), name="comments-detail")
]
