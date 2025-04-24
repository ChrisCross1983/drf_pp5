from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField()
    sitting_request_id = serializers.SerializerMethodField()
    sender_profile_id = serializers.SerializerMethodField()
    comment_id = serializers.SerializerMethodField() 

    class Meta:
        model = Notification
        fields = [
            'id', 'message', 'is_read', 'created_at', 'type',
            'post_id', 'sitting_request_id', 'sender_profile_id', 'comment_id'
        ]

    def get_post_id(self, obj):
        return obj.post.id if obj.post else None

    def get_sitting_request_id(self, obj):
        return obj.sitting_request.id if obj.sitting_request else None

    def get_sender_profile_id(self, obj):
        return obj.sender_profile.id if obj.sender_profile else None

    def get_comment_id(self, obj):
        return obj.comment.id if hasattr(obj, "comment") and obj.comment else None
