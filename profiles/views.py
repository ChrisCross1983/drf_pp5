from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.middleware.csrf import get_token
from dj_rest_auth.views import LogoutView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.db.models import Count
from django.conf import settings
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly

def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

class RegisterView(CreateAPIView):
    """
    Endpoint to register a new user.
    """
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CurrentUserProfileView(APIView):
    """
    Endpoint to retrieve the profile of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class UserProfileView(RetrieveAPIView):
    """
    Endpoint to retrieve the profile of a specific user by ID.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

class EditProfileView(RetrieveUpdateAPIView):
    """
    Endpoint to allow users to edit their profile details.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    permission_classes = [IsAuthenticated]

class CustomLogoutView(LogoutView):
    """
    Custom logout view using Django session authentication.
    """
    permission_classes = [IsAuthenticated]

class FollowUserView(APIView):
    """
    Endpoint to follow or unfollow another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            target_profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if target_profile.user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.profile in target_profile.followers.all():
            target_profile.followers.remove(request.user.profile)
            return Response({"message": "Unfollowed successfully."}, status=status.HTTP_200_OK)
        else:
            target_profile.followers.add(request.user.profile)
            return Response({"message": "Followed successfully."}, status=status.HTTP_200_OK)

class FollowersListView(APIView):
    """
    Endpoint to get a list of followers for a user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        followers = profile.followers.all()
        data = [{"id": follower.id, "username": follower.user.username} for follower in followers]
        return Response(data, status=status.HTTP_200_OK)

class FollowingListView(APIView):
    """
    Endpoint to get a list of profiles the user is following.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        following = profile.following.all()
        data = [{"id": follow.id, "username": follow.user.username} for follow in following]
        return Response(data, status=status.HTTP_200_OK)

class TopFollowedProfilesView(APIView):
    """
    Endpoint to retrieve the top 5 most-followed profiles.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        top_profiles = Profile.objects.annotate(follower_count=Count('followers')).order_by('-follower_count')[:5]
        data = [
            {
                "id": profile.id,
                "username": profile.user.username,
                "follower_count": profile.follower_count,
                "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
            }
            for profile in top_profiles
        ]
        return Response(data, status=status.HTTP_200_OK)
