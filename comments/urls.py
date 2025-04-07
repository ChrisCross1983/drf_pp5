from django.urls import path
from comments import views

urlpatterns = [
    path('', views.CommentList.as_view(), name="comments-list"),
    path('<int:pk>/', views.CommentDetail.as_view(), name="comments-detail")
]
