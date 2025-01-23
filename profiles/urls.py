from django.urls import path
from .views import RegisterView, UserProfileView, CurrentUserProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair   '),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('<int:pk>/', UserProfileView.as_view(), name='user-profile'),
]
