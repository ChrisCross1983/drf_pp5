from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.middleware.csrf import get_token
from dj_rest_auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.db.models import Count
from django.conf import settings
from .models import Profile
from posts.models import Notification
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

class CustomLoginView(LoginView):
    def options(self, request, *args, **kwargs):
        """Antwort auf eine CORS Preflight OPTIONS-Anfrage."""
        response = JsonResponse({"message": "CORS preflight successful"})
        response["Access-Control-Allow-Origin"] = request.headers.get("Origin", "")
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

class CurrentUserProfileView(APIView):
    """
    Endpoint to retrieve the profile of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)

class UserProfileView(RetrieveAPIView):
    """
    Endpoint to retrieve the profile of a specific user by ID.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        """Ensure the request is passed for is_following calculation."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

class EditProfileView(RetrieveUpdateAPIView):
    """
    Endpoint to allow users to edit their profile details.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_context(self):
        """Ensure the request is passed for is_following calculation."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

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

            Notification.objects.create(
                user=target_profile.user,
                type="follow",
                message=f"{request.user.username} started following you."
            )

            return Response({"message": "Followed successfully."}, status=status.HTTP_200_OK)

class FollowersListView(ListAPIView):
    """
    Endpoint to get a list of followers for a user.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile_id = self.kwargs.get("pk")
        return Profile.objects.filter(following__id=profile_id)

class FollowingListView(ListAPIView):
    """
    Endpoint to get a list of profiles the user is following.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile_id = self.kwargs.get("pk")
        return Profile.objects.get(pk=profile_id).following.all()

class TopFollowedProfilesView(ListAPIView):
    """
    API View to get the top 5 most-followed profiles.
    """
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Profile.objects.annotate(
            follower_count=Count("followers")
        ).order_by("-follower_count")[:5]
