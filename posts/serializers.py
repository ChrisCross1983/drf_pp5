from rest_framework import serializers
from .models import Post, Comment, SittingRequest, Notification

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'is_owner']

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and request.user == obj.author


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'description', 'image', 'author',
            'likes_count', 'comments', 'created_at', 'is_owner'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and request.user == obj.author


class SittingRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = SittingRequest
        fields = [
            'id', 'sender', 'receiver', 'post', 'message', 'status',
            'created_at', 'sender_username', 'receiver_username', 'post_title'
        ]
        read_only_fields = ['id', 'sender', 'receiver', 'post', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'type', 'post', 'message', 'is_read', 'created_at']
