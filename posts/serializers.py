from rest_framework import serializers
from .models import Post, Comment, SittingRequest


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'description', 'image', 'author', 'likes_count', 'comments', 'created_at']
    def get_likes_count(self, obj):
        return obj.likes.count()

class SittingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SittingRequest
        fields = ['id', 'sender', 'receiver', 'post', 'message', 'created_at']
        read_only_fields = ['id', 'sender', 'receiver', 'post', 'created_at']
