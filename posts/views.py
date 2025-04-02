from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from profiles.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Post, Comment, SittingRequest
from likes.models import Like
from .serializers import PostSerializer, CommentSerializer, SittingRequestSerializer
from notifications.models import Notification
import logging

logger = logging.getLogger(__name__)


class AllPosts(APIView):
    def get(self, request):
        return Response({"message": "All posts endpoint works!"})


class PostFeedPagination(PageNumberPagination):
    page_size = 10


class CreatePostView(CreateAPIView):
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        logger.info(f"📝 User {self.request.user} creating post.")
        serializer.save(author=self.request.user)


class PostFeedView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostFeedPagination
    permission_classes = [AllowAny]

    def get_queryset(self):

        try:
            queryset = Post.objects.annotate(
                likes_count=Count('likes', distinct=True),
                comments_count=Count('comments', distinct=True)
            )

            search_query = self.request.query_params.get('search')
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query)
                )

            category_filter = self.request.query_params.get('category')
            if category_filter:
                queryset = queryset.filter(category=category_filter)

            ordering = self.request.query_params.get('ordering', '-created_at')
            queryset = queryset.order_by(ordering)

            return queryset

        except Exception as e:
            logger.error(f"❌ ERROR in get_queryset(): {str(e)}", exc_info=True)
            return Post.objects.none()


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}


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
        }, status=status.HTTP_200_OK)


class ListCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")


class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = CommentSerializer(data=request.data, context={"request": request})

            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("❌ Comment Creation Error")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_context(self):
        return {"request": self.request}


class CreateSittingRequestView(APIView):
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
        except Exception as e:
            logger.exception("❌ Unexpected error in CreateSittingRequestView")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SentSittingRequestsView(generics.ListAPIView):
    serializer_class = SittingRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SittingRequest.objects.filter(sender=self.request.user)


class IncomingSittingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sitting_requests = SittingRequest.objects.filter(receiver=request.user)
        serializer = SittingRequestSerializer(sitting_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageSittingRequestView(APIView):
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
