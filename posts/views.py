from django.db import models
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from profiles.permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

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