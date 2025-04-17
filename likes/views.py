from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from posts.models import Post
from likes.models import Like
from notifications.models import Notification 
from likes.serializers import LikeSerializer

class PostLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(owner=request.user, post=post)
        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
    
        if post.author != request.user:
            Notification.objects.create(
                user=post.author,
                sender=request.user,
                type="like",
                post=post,
                message=f"{request.user.username} liked your post."
            )

        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Like.objects.filter(owner=request.user, post=post).first()
        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
