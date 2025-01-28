from django.urls import path, include
from django.contrib.auth import views as auth_views
from dj_rest_auth.views import LoginView, LogoutView
from profiles.views import CustomLogoutView
from .views import (
    RegisterView,
    UserProfileView,
    CurrentUserProfileView,
    EditProfileView,
    CustomPasswordChangeView,
    FollowUserView,
    FollowersListView,
    FollowingListView,
    TopFollowedProfilesView,
    csrf_token_view,
)

urlpatterns = [
    path("auth/csrf/", csrf_token_view, name="csrf-token"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name="logout"),
    path('me/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('edit/', EditProfileView.as_view(), name='edit-profile'),
    path('<int:pk>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<int:pk>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('<int:pk>/following/', FollowingListView.as_view(), name='following-list'),
    path('top-followed/', TopFollowedProfilesView.as_view(), name='top-followed-profiles'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
]
