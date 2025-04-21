from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import (
    RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Count, F, Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from dj_rest_auth.serializers import JWTSerializer
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import ResendEmailVerificationView
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation

from likes.models import Like, CommentLike
from posts.models import Post, SittingRequest
from comments.models import Comment
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly

import logging

logger = logging.getLogger(__name__)


def csrf_token_view(request):
    response = JsonResponse({"csrfToken": get_token(request)})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "Authorization, Content-Type, X-CSRFToken"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


class RegisterView(CreateAPIView):
    """
    Endpoint to register a new user.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def post(self, request, *args, **kwargs):
        print("📂 REGISTER REQUEST FILES:", request.FILES)
        print("📦 REGISTER REQUEST DATA:", request.data)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            send_email_confirmation(request, user)

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "User registered successfully! Verification email sent.",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        try:
            confirmation = self.get_object()
            confirmation.confirm(request)
            logger.info("✅ Email successfully verified.")

            frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
            return redirect("/login?verified=true")

        except self.model.DoesNotExist:
            logger.warning("⚠️ Verification link invalid or expired.")
            return redirect(f"{frontend_url}/login?expired=true")


class CustomResendEmailView(ResendEmailVerificationView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({"message": "A new verification email has been sent."})


class CustomLoginView(LoginView):
    """
    Custom Login View, that ensures JWT Authentification.
    """
    def post(self, request, *args, **kwargs):
        print("✅ CustomLoginView is being used!")
        response = super().post(request, *args, **kwargs)

        if "key" in response.data:
            print("🔴 Only 'key' received! Generating JWT manually...")

            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)

        print("🔄 Login Response Data:", response.data)
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
    queryset = Profile.objects.annotate(
        total_posts=Count('user__user_posts', distinct=True),
        followers_count=Count('followers', distinct=True),
        following_count=Count('following', distinct=True)
    )
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

    def patch(self, request, *args, **kwargs):
        from rest_framework import status, generics, permissions
        print("📂 Uploaded files (EditProfileView):", request.FILES)
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user.profile

    def get_serializer_context(self):
        """Ensure the request is passed for is_following calculation."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class DeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User and profile deleted."}, status=status.HTTP_204_NO_CONTENT)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    permission_classes = [IsAuthenticated]


class CustomLogoutView(APIView):
    """
    Custom Logout View, that blacklists Refresh-Tokens.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            target_profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if target_profile.user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = request.user.profile

        if user_profile in target_profile.followers.all():
            target_profile.followers.remove(user_profile)
            message = "Unfollowed successfully."
        else:
            target_profile.followers.add(user_profile)
            message = "Followed successfully."

            if target_profile.user != request.user:
                Notification.objects.create(
                    user=target_profile.user,
                    type="follow",
                    message=f"{request.user.username} started following you."
                )

        return Response({"message": message}, status=status.HTTP_200_OK)


class FollowersListView(ListAPIView):
    """
    Endpoint to get a list of followers for a user.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile_id = self.kwargs.get("pk")
        return Profile.objects.filter(following__id=profile_id).annotate(
            total_posts=Count("user__user_posts", distinct=True),
            followers_count=Count("followers", distinct=True),
            following_count=Count("following", distinct=True)
        )


class FollowingListView(ListAPIView):
    """
    Endpoint to get a list of profiles the user is following.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        profile_id = self.kwargs.get("profile_id")
        try:
            return Profile.objects.get(pk=profile_id).following.annotate(
                total_posts=Count("user__user_posts", distinct=True),
                followers_count=Count("followers", distinct=True),
                following_count=Count("following", distinct=True)
            )
        except Profile.DoesNotExist:
            return Profile.objects.none()


class TopFollowedProfilesView(ListAPIView):
    """
    API View to get the top 5 most-followed profiles.
    """
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Profile.objects.annotate(
            total_posts=Count("user__user_posts", distinct=True),
            followers_count=Count("followers", distinct=True),
            following_count=Count("following", distinct=True)
        ).order_by("-followers_count")[:5]


class ProfileKPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        total_posts = Post.objects.filter(author=user).count()
        total_followers = user.profile.followers.count()
        total_following = user.profile.following.count()

        in_requests = SittingRequest.objects.filter(receiver=user).count()
        out_requests = SittingRequest.objects.filter(sender=user).count()

        valid_comments = Comment.objects.filter(
            post__author=user
        ).exclude(owner=user)
        
        post_likes = Like.objects.filter(post__author=user).count()
        comment_ids = Comment.objects.filter(post__author=user).exclude(owner=user).values_list("id", flat=True)
        comment_likes = CommentLike.objects.filter(comment__in=comment_ids).count()
        total_likes = post_likes + comment_likes

        total_comments = valid_comments.count()

        return Response({
            "total_posts": total_posts,
            "followers": total_followers,
            "following": total_following,
            "comments": total_comments,
            "likes": total_likes,
            "likes_on_posts": post_likes,
            "likes_on_comments": comment_likes,
            "requests_in": in_requests,
            "requests_out": out_requests,
        })
