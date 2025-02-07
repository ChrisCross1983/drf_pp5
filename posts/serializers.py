from rest_framework import serializers
from .models import Post, Comment, SittingRequest
import notifications.models

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_owner = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'is_owner']

    def get_is_owner(self, obj):
        request = self.context.get("request", None)
        return request.user == obj.author if request and request.user.is_authenticated else False

    def create(self, validated_data):
        post = validated_data.pop('post')
        comment = Comment.objects.create(post=post, **validated_data)
        return comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    has_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    category = serializers.ChoiceField(
        choices=[
            ('offer', 'Offer Sitting'),
            ('search', 'Search Sitting'),
            ('general', 'General'),
        ]
    )

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'description', 'image', 'author',
            'likes_count', 'has_liked', 'comments', 'created_at', 'is_owner'
        ]

    def get_likes_count(self, obj):
        return obj.post_likes.count()

    def get_has_liked(self, obj):
        request = self.context.get("request")
        return request and request.user.is_authenticated and obj.likes.filter(user=request.user).exists()

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
        read_only_fields = ['id', 'sender', 'receiver', 'created_at']

    def create(self, validated_data):
        request = self.context.get("request")
        post = validated_data.pop("post")

        if SittingRequest.objects.filter(sender=request.user, post=post).exists():
            raise serializers.ValidationError("You have already sent a request for this post.")

        sitting_request = SittingRequest.objects.create(
            sender=request.user,
            receiver=post.author,
            post=post,
            **validated_data
        )
        return sitting_request
