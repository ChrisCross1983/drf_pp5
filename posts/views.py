
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from profiles.permissions import IsOwnerOrReadOnly
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Post, Comment, SittingRequest, Like
from .serializers import PostSerializer, CommentSerializer, SittingRequestSerializer
import notifications.models

import logging
logger = logging.getLogger(__name__)

class PostFeedPagination(PageNumberPagination):
    page_size = 10

class CreatePostView(CreateAPIView):
    """
    API View to create a new post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        logger.info(f"📝 CreatePostView: User {self.request.user} is creating a post.")

        if self.request.user.is_authenticated:
            logger.info(f"🔍 `request.user` ist: {self.request.user.id} ({self.request.user.username})")
        else:
            logger.warning(f"⚠️ `request.user` ist NOT SET!")

        try:
            serializer.save(author=self.request.user)
            logger.info(f"✅ Post successfully created by {self.request.user}")
        except Exception as e:
            logger.exception(f"❌ Error while creating post: {str(e)}")
        return Response({"error": "Failed to create post."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostFeedView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get_queryset(self):
        logger.info("📌 PostFeedView: get_queryset() started")

        try:
            queryset = Post.objects.all()
            logger.info(f"✅ Number of posts in DB: {queryset.count()}")

            search_query = self.request.query_params.get('search')
            if search_query:
                logger.info(f"🔍 Search query: {search_query}")
                queryset = queryset.filter(
                    models.Q(title__icontains=search_query) |
                    models.Q(description__icontains=search_query)
                )

            category_filter = self.request.query_params.get('category')
            if category_filter:
                logger.info(f"📂 Category filter: {category_filter}")
                queryset = queryset.filter(category=category_filter)

            ordering = self.request.query_params.get('ordering', '-created_at')
            logger.info(f"📏 Ordering: {ordering}")
            queryset = queryset.order_by(ordering)

            logger.info("✅ get_queryset() completed successfully")
            return queryset

        except Exception as e:
            logger.error(f"❌ ERROR in get_queryset(): {str(e)}", exc_info=True)
            return Post.objects.none()

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {"request": self.request}
    
    def put(self, request, *args, **kwargs):
        logger.info(f"PUT-Request von {request.user}")
        return super().put(request, *args, **kwargs)

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

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
        print(f"🔍 DELETE REQUEST: User {request.user} (ID: {request.user.id}) tried, Like for Post {post.id} to delete.")
        
        like = Like.objects.filter(post=post, user=request.user)

        print(f"🔍 DELETE REQUEST: User {request.user} tried, Like for Post {post.id} to delete.")

        if not like.exists():
            print(f"⚠️ ATTENTION: No Like found for User {request.user} on Post {post.id}")
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"✅ Like existiert. Likes BEFORE deleting: {Like.objects.filter(post=post).count()}")

        like.delete()
        post.likes.remove(request.user)

        print(f"✅ Like deleted! Likes AFTER deleting: {Like.objects.filter(post=post).count()}")

        if Like.objects.filter(post=post, user=request.user).exists():
            print(f"❌ ERROR: Like wasnt correct removed!")
            return Response({"detail": "Error: Like was not removed properly."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "detail": "Like removed!",
            "likes_count": post.likes.count(),
            "has_liked": False
        }, status=status.HTTP_200_OK)

class ListCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        return Comment.objects.filter(post_id=post_id).order_by("-created_at") 

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
        print(f"🔍 Incoming Comment Data: {request.data}")

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
        logger.info(f"🐾 SittingRequest: Start for Post ID {post_id} by User {request.user}")

        try:
            post = Post.objects.get(pk=post_id)
            logger.info(f"✅ Post found: {post.title} (Author: {post.author.username})")

            # Prevent users from requesting their own posts
            if post.author == request.user:
                logger.warning(f"🚫 User {request.user} attempted to request their own post.")
                return Response({"error": "You cannot request sitting for your own post."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user already sent a request
            existing_request = SittingRequest.objects.filter(sender=request.user, post=post).first()
            print(f"Checking SittingRequest: User={request.user.username}, Post={post.id}, Found={existing_request}")
            if existing_request:
                logger.warning(f"⚠️ Duplicate request detected for User {request.user} on Post {post_id}.")
                return Response({"error": "You have already sent a request for this post."}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize request data
            serializer = SittingRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sender=request.user, receiver=post.author, post=post)
                logger.info(f"🎉 SittingRequest successfully created by {request.user} for Post {post_id}")

                # Create a notification
                Notification.objects.create(
                    user=post.author,
                    type="request",
                    sitting_request=serializer.instance,
                    message=f"{request.user.username} has sent a sitting request for your post."
                )
                logger.info(f"🔔 Notification sent to {post.author.username}.")

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.error(f"❌ SittingRequest validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            logger.error(f"❌ Post with ID {post_id} not found!")
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"❌ Unexpected error in CreateSittingRequestView: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
