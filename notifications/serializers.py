from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField()
    sender_profile_id = serializers.SerializerMethodField()
    sitting_request_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at', 'type',
                  'post_id', 'sender_profile_id', 'sitting_request_id']

    def get_post_id(self, obj):
        if obj.type in ['comment', 'like'] and hasattr(obj, 'sitting_request') and obj.sitting_request:
            return obj.sitting_request.post.id
        elif obj.type in ['comment', 'like'] and hasattr(obj, 'post'):
            return obj.post.id
        return None

    def get_sender_profile_id(self, obj):
        return getattr(obj, "sender_profile_id", None)

    def get_sitting_request_id(self, obj):
        if obj.sitting_request:
            return obj.sitting_request.id
        return None
