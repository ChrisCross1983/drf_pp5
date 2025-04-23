from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from itertools import chain
from operator import itemgetter

from posts.models import Post, SittingRequest
from comments.models import Comment
from likes.models import Like, CommentLike
from profiles.models import FollowRequest
from profiles.serializers import ProfileMiniSerializer
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer

class ActivityFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        post_activities = [
            {
                "type": "post",
                "message": f"You created a post: '{p.title}'",
                "timestamp": p.created_at,
                "data": {"post_id": p.id}
            } for p in Post.objects.filter(author=user)
        ]

        comment_activities = [
            {
                "type": "comment",
                "message": f"You commented on a post",
                "timestamp": c.created_at,
                "data": {"comment_id": c.id, "post_id": c.post.id}
            } for c in Comment.objects.filter(owner=user)
        ]

        post_like_activities = [
            {
                "type": "like",
                "message": f"You liked a post",
                "timestamp": l.created_at,
                "data": {"post_id": l.post.id}
            } for l in Like.objects.filter(owner=user)
        ]

        comment_like_activities = [
            {
                "type": "like",
                "message": f"You liked a comment",
                "timestamp": l.created_at,
                "data": {"comment_id": l.comment.id}
            } for l in CommentLike.objects.filter(owner=user)
        ]

        follow_sent = [
            {
                "type": "follow",
                "message": f"You sent a follow request to {r.receiver.user.username}",
                "timestamp": r.created_at,
                "data": {"to_user": r.receiver.id}
            } for r in FollowRequest.objects.filter(sender=user.profile)
        ]

        follow_accepted = [
            {
                "type": "follow_accepted",
                "message": f"{r.sender.user.username} accepted your follow request",
                "timestamp": r.updated_at,
                "data": {"from_user": r.sender.id}
            } for r in FollowRequest.objects.filter(receiver=user.profile, status="accepted")
        ]

        sitting_requests = [
            {
                "type": "sitting",
                "message": f"You sent a sitting request to {sr.receiver.username}",
                "timestamp": sr.created_at,
                "data": {"sitting_id": sr.id}
            } for sr in SittingRequest.objects.filter(sender=user)
        ]

        all_activities = list(chain(
            post_activities,
            comment_activities,
            post_like_activities,
            comment_like_activities,
            follow_sent,
            follow_accepted,
            sitting_requests
        ))

        sorted_activities = sorted(all_activities, key=itemgetter("timestamp"), reverse=True)

        return Response(sorted_activities)
