from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from itertools import chain
from operator import itemgetter

from posts.models import Post, SittingRequest
from comments.models import Comment
from likes.models import Like, CommentLike
from profiles.models import FollowRequest

PLACEHOLDER = "https://res.cloudinary.com/daj7vkzdw/image/upload/v1744729686/Placeholder/hshdlbr977dc6dq9gt2o.jpg"


class ActivityFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get_pic(self, profile):
        return (
            profile.profile_picture.url
            if hasattr(profile, "profile_picture") and profile.profile_picture
            else PLACEHOLDER
        )

    def get(self, request):
        user = request.user

        post_activities = [
            {
                "type": "post",
                "message": "You created a post",
                "timestamp": p.created_at,
                "data": {
                    "post_id": p.id,
                    "title": p.title or "Untitled",
                    "image": p.image.url if p.image else None
                }
            } for p in Post.objects.filter(author=user)
        ]

        comment_activities = [
            {
                "type": "comment",
                "message": "You commented on a post",
                "timestamp": c.created_at,
                "data": {
                    "comment_id": c.id,
                    "content": (c.content[:60] + "...") if len(c.content) > 60 else c.content,
                    "post_id": c.post.id,
                    "post_title": c.post.title or "Untitled",
                    "post_image": c.post.image.url if c.post.image else None
                }
            }
            for c in Comment.objects.filter(owner=user).select_related("post")
            if c.post
        ]

        post_like_activities = [
            {
                "type": "like",
                "message": "You liked a post",
                "timestamp": l.created_at,
                "data": {
                    "post_id": l.post.id,
                    "title": l.post.title or "Untitled",
                    "image": l.post.image.url if l.post.image else None
                }
            }
            for l in Like.objects.filter(owner=user).select_related("post")
            if l.post
        ]

        comment_like_activities = [
            {
                "type": "like_comment",
                "message": "You liked a comment",
                "timestamp": l.created_at,
                "data": {
                    "comment_id": l.comment.id,
                    "post_id": l.comment.post.id,
                    "content": (l.comment.content[:60] + "...") if len(l.comment.content) > 60 else l.comment.content,
                    "post_title": l.comment.post.title or "Untitled"
                }
            }
            for l in CommentLike.objects.filter(owner=user).select_related("comment__post")
            if l.comment and l.comment.post
        ]

        follow_sent = [
            {
                "type": "follow",
                "message": f"You sent a follow request to {r.receiver.user.username}",
                "timestamp": r.created_at,
                "data": {
                    "user_id": r.receiver.id,
                    "username": r.receiver.user.username,
                    "first_name": r.receiver.user.first_name,
                    "last_name": r.receiver.user.last_name,
                    "profile_picture": self.get_pic(r.receiver)
                }
            }
            for r in FollowRequest.objects.filter(sender=user.profile).select_related("receiver__user")
        ]

        follow_accepted = [
            {
                "type": "follow_accepted",
                "message": f"{r.sender.user.username} accepted your follow request",
                "timestamp": r.created_at,
                "data": {
                    "user_id": r.sender.id,
                    "username": r.sender.user.username,
                    "first_name": r.sender.user.first_name,
                    "last_name": r.sender.user.last_name,
                    "profile_picture": self.get_pic(r.sender)
                }
            }
            for r in FollowRequest.objects.filter(receiver=user.profile, status="accepted").select_related("sender__user")
        ]

        sitting_requests = [
            {
                "type": "sitting",
                "message": f"You sent a sitting request to {sr.receiver.username}",
                "timestamp": sr.created_at,
                "data": {
                    "sitting_id": sr.id,
                    "receiver_id": sr.receiver.profile.id if hasattr(sr.receiver, "profile") else None,
                    "receiver_username": sr.receiver.username,
                    "profile_picture": self.get_pic(sr.receiver.profile) if hasattr(sr.receiver, "profile") else PLACEHOLDER
                }
            } for sr in SittingRequest.objects.filter(sender=user).select_related("receiver__profile")
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
