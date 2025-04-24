from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from itertools import chain
from operator import itemgetter

from posts.models import Post, SittingRequest
from comments.models import Comment
from likes.models import Like, CommentLike
from profiles.models import FollowRequest

class ActivityFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        post_activities = [
            {
                "type": "post",
                "message": f"You created the post “{p.title}”",
                "timestamp": p.created_at,
                "data": {
                    "post_id": p.id,
                    "post_title": p.title
                }
            } for p in Post.objects.filter(author=user) if p.title
        ]

        comment_activities = [
            {
                "type": "comment",
                "message": f"You commented: “{c.content}”",
                "timestamp": c.created_at,
                "data": {
                    "comment_id": c.id,
                    "post_id": c.post.id,
                    "post_title": c.post.title,
                    "content": c.content
                }
            } for c in Comment.objects.filter(owner=user) if c.content
        ]

        post_like_activities = [
            {
                "type": "like",
                "message": f"You liked the post “{l.post.title}”",
                "timestamp": l.created_at,
                "data": {
                    "post_id": l.post.id,
                    "post_title": l.post.title
                }
            } for l in Like.objects.filter(owner=user) if l.post and l.post.title
        ]

        comment_like_activities = [
            {
                "type": "like",
                "message": f"You liked a comment: “{l.comment.content}”",
                "timestamp": l.created_at,
                "data": {
                    "comment_id": l.comment.id,
                    "post_id": l.comment.post.id,
                    "post_title": l.comment.post.title,
                    "comment_content": l.comment.content
                }
            } for l in CommentLike.objects.filter(owner=user) if l.comment and l.comment.content
        ]

        follow_sent = [
            {
                "type": "follow",
                "message": f"You sent a follow request to {r.receiver.user.username}",
                "timestamp": r.created_at,
                "data": {
                    "to_user": r.receiver.id,
                    "username": r.receiver.user.username,
                    "first_name": r.receiver.user.first_name,
                    "last_name": r.receiver.user.last_name,
                    "profile_picture": (
                        r.receiver.profile_picture.url
                        if r.receiver.profile_picture
                        else "https://res.cloudinary.com/daj7vkzdw/image/upload/v1744729686/Placeholder/hshdlbr977dc6dq9gt2o.jpg"
                    )
                }
            }
            for r in FollowRequest.objects.filter(sender=user.profile)
        ]

        follow_accepted = [
            {
                "type": "follow_accepted",
                "message": f"{r.sender.user.username} accepted your follow request",
                "timestamp": r.created_at,
                "data": {
                    "from_user": r.sender.id,
                    "username": r.sender.user.username,
                    "first_name": r.sender.user.first_name,
                    "last_name": r.sender.user.last_name,
                    "profile_picture": (
                        r.sender.profile_picture.url
                        if r.sender.profile_picture
                        else "https://res.cloudinary.com/daj7vkzdw/image/upload/v1744729686/Placeholder/hshdlbr977dc6dq9gt2o.jpg"
                    )
                }
            }
            for r in FollowRequest.objects.filter(receiver=user.profile, status="accepted")
        ]

        sitting_requests = [
            {
                "type": "sitting",
                "message": f"You sent a sitting request to {sr.receiver.username}",
                "timestamp": sr.created_at,
                "data": {
                    "sitting_id": sr.id,
                    "receiver_id": sr.receiver.id,
                    "receiver_username": sr.receiver.username
                }
            } for sr in SittingRequest.objects.filter(sender=user) if sr.receiver
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
