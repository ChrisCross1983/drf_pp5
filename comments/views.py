from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from profiles.permissions import IsOwnerOrReadOnly
from notifications.models import Notification
from posts.models import Post
from .models import Comment
from .pagination import CommentPagination
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
    pagination_class = CommentPagination

    def get_queryset(self):
        return Comment.objects.filter(parent__isnull=True).order_by("-created_at")

    def perform_create(self, serializer):
        comment = serializer.save(owner=self.request.user)

        if comment.post.author != self.request.user:
            Notification.objects.create(
                user=comment.post.author,
                type="comment",
                message=f"{self.request.user.username} commented on your post: “{comment.content[:30]}...”",
                post=comment.post
            )


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a comment, or update or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        post = instance.post
        self.perform_destroy(instance)

        post.save(update_fields=[])

        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleCommentLike(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True

            if request.user != comment.owner:
                Notification.objects.create(
                    user=comment.owner,
                    type="like",
                    comment=comment,
                    message=f"{request.user.username} liked your comment: “{comment.content[:30]}...”",
                )

        return Response({
            "liked": liked,
            "likes_count": comment.likes.count(),
        }, status=status.HTTP_200_OK)
