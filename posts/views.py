from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from profiles.permissions import IsOwnerOrReadOnly
from .models import Post, Comment, SittingRequest, Like
import notifications.models

from .serializers import PostSerializer, CommentSerializer, SittingRequestSerializer

import logging
logger = logging.getLogger(__name__)

class PostFeedPagination(PageNumberPagination):
    page_size = 10

class CreatePostView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostFeedView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PostFeedPagination

    def get_queryset(self):
        try:
            queryset = super().get_queryset()

            search_query = self.request.query_params.get('search')
            if search_query:
                queryset = queryset.filter(
                    models.Q(title__icontains=search_query) |
                    models.Q(description__icontains=search_query)
                )

            category_filter = self.request.query_params.get('category')
            if category_filter:
                queryset = queryset.filter(category=category_filter)

            ordering = self.request.query_params.get('ordering', '-created_at')
            queryset = queryset.order_by(ordering)

            return queryset
        except Exception as e:
            logger.error(f"🔥 Error in PostFeedView: {e}")
            return Post.objects.none()

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        existing_like = Like.objects.filter(post=post, user=request.user).first()

        if existing_like:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(post=post, user=request.user)
        post.likes.add(request.user)

        return Response({
            "detail": "Post liked!",
            "likes_count": post.likes.count(),
            "has_liked": True
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user)

        if not like.exists():
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        post.likes.remove(request.user)
        return Response({
            "detail": "Like removed!",
            "likes_count": post.likes.count(),
            "has_liked": False
        }, status=status.HTTP_204_NO_CONTENT)

class ListCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        return Comment.objects.filter(post_id=post_id)

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Fetch all comments for a specific post.
        """
        try:
            post = Post.objects.get(pk=pk)
            comments = Comment.objects.filter(post=post).order_by("-created_at")
            serializer = CommentSerializer(comments, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        print("🔍 Incoming Comment Data:", request.data)

        try:
            post = Post.objects.get(pk=pk)
            serializer = CommentSerializer(data=request.data, context={"request": request})

            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            print("⚠️ Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("❌ Comment Creation Error:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}
    
    def put(self, request, *args, **kwargs):
        logger.info(f"PUT-Request von {request.user}")
        return super().put(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    Endpoint to allow users to edit or delete their comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}

class CreateSittingRequestView(APIView):
    """
    API View to create a sitting request for a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)

            if post.author == request.user:
                return Response({"error": "You cannot request sitting for your own post."}, status=status.HTTP_400_BAD_REQUEST)

            existing_request = SittingRequest.objects.filter(sender=request.user, post=post).first()
            if existing_request:
                return Response({"error": "You have already sent a request for this post."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = SittingRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sender=request.user, receiver=post.author, post=post)

                Notification.objects.create(
                    user=post.author,
                    type="request",
                    sitting_request=serializer.instance,
                    message=f"{request.user.username} has sent a sitting request for your post."
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class SentSittingRequestsView(generics.ListAPIView):
    serializer_class = SittingRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SittingRequest.objects.filter(sender=self.request.user)

class IncomingSittingRequestsView(APIView):
    """
    API View to get incoming sitting requests.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sitting_requests = SittingRequest.objects.filter(receiver=request.user)
        serializer = SittingRequestSerializer(sitting_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ManageSittingRequestView(APIView):
    """
    API View to accept/decline sitting requests.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            sitting_request = SittingRequest.objects.get(pk=request_id, receiver=request.user)
            action = request.data.get("action")

            if action == "accept":
                sitting_request.status = "accepted"
                message = "Request accepted."
            elif action == "decline":
                sitting_request.status = "declined"
                message = "Request declined."
            else:
                return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

            sitting_request.save()

            Notification.objects.create(
                user=sitting_request.sender,
                type="request",
                sitting_request=sitting_request,
                message=f"Your sitting request was {sitting_request.status}."
            )

            return Response({"message": message, "status": sitting_request.status}, status=status.HTTP_200_OK)

        except SittingRequest.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)
