from django.urls import path
from dj_rest_auth.views import UserDetailsView
from django.contrib.auth import views as auth_views
from allauth.account.views import ConfirmEmailView
from .views import (
    CustomLoginView,
    RegisterView,
    CustomResendEmailView,
    UserProfileView,
    CurrentUserProfileView,
    EditProfileView,
    CustomPasswordChangeView,
    FollowUserView,
    FollowersListView,
    FollowingListView,
    TopFollowedProfilesView,
    ProfileKPIView,
)

urlpatterns = [
    path("auth/user/", UserDetailsView.as_view(), name="user-details"),
    path("kpis/", ProfileKPIView.as_view(), name="profile-kpis"),
    path("auth/registration/", RegisterView.as_view(), name="custom-registration"),
    path('me/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('edit/', EditProfileView.as_view(), name='edit-profile'),
    path('<int:pk>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<int:pk>/followers/', FollowersListView.as_view(), name='followers-list'),
    path('<int:pk>/following/', FollowingListView.as_view(), name='following-list'),
    path('top-followed/', TopFollowedProfilesView.as_view(), name='top-followed-profiles'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
