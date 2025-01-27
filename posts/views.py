from django.db import models
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from profiles.permissions import IsOwnerOrReadOnly
from .models import Post, Comment, SittingRequest
from .serializers import PostSerializer, CommentSerializer, SittingRequestSerializer

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

        return queryset

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(request.user)
            return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)

class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    Endpoint to allow users to edit or delete their comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CreateSittingRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        print("DEBUG: Entered CreateSittingRequestView with post_id:", post_id)
        print("DEBUG: Request user:", request.user)
        print("DEBUG: Request data:", request.data)
        try:
            post = Post.objects.get(pk=post_id)
            print("Post found:", post.title)
            if post.author == request.user:
                return Response({"error": "You cannot request sitting for your own post."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = SittingRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sender=request.user, receiver=post.author, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Post.DoesNotExist:
            print("DEBUG: Post with id", post_id, "not found.")
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class IncomingSittingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incoming_requests = SittingRequest.objects.filter(receiver=request.user)
        serializer = SittingRequestSerializer(incoming_requests, many=True)
        return Response(serializer.data)


class ManageSittingRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            sitting_request = SittingRequest.objects.get(id=request_id, receiver=request.user)
            action = request.data.get('action')
            
            if action == 'accept':
                sitting_request.status = 'accepted'
            elif action == 'decline':
                sitting_request.status = 'declined'
            else:
                return Response({'error': 'Invalid action'}, status=400)
            
            sitting_request.save()
            return Response({'message': f'Request {action}ed successfully.'})
        except SittingRequest.DoesNotExist:
            return Response({'error': 'Request not found'}, status=404)
