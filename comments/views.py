from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from profiles.permissions import IsOwnerOrReadOnly
from notifications.models import Notification
from posts.models import Post
from .models import Comment
from .serializers import CommentDetailSerializer
from comments.serializers import CommentSerializer


class CommentList(generics.ListCreateAPIView):
    """
    List comments or create a comment if logged in.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

    def perform_create(self, serializer):
        comment = serializer.save(owner=self.request.user)

        if comment.post.author != self.request.user:
            Notification.objects.create(
                user=comment.post.author,
                type="comment",
                message=f"{self.request.user.username} commented on your post: “{comment.content[:30]}...”",
            )


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
