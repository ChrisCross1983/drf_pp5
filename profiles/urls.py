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
from .views_follow_requests import (
    FollowRequestListView,
    FollowRequestCreateView,
    FollowRequestRespondView,
    FollowRequestCancelView,
    UnfollowView,
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

    # Follow Request Endpoints
    path("follow-requests/", FollowRequestListView.as_view(), name="follow-requests-list"),
    path("follow-requests/send/<int:target_id>/", FollowRequestCreateView.as_view(), name="follow-request-send"),
    path("follow-requests/manage/<int:request_id>/", FollowRequestRespondView.as_view(), name="follow-request-manage"),
    path("follow-requests/cancel/<int:request_id>/", FollowRequestCancelView.as_view(), name="follow-request-cancel"),
    path("profiles/unfollow/<int:target_id>/", UnfollowView.as_view(), name="unfollow"),
]
