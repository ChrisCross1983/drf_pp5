from rest_framework import serializers
from .models import Post, Comment, SittingRequest


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    is_owner = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)
    author_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "author_image", "post", "content", "created_at", "is_owner"]

    def get_is_owner(self, obj):
        request = self.context.get("request", None)
        return request.user == obj.author if request and request.user.is_authenticated else False

    def get_author_image(self, obj):
        profile = getattr(obj.author, "profile", None)
        if not profile or not hasattr(profile, "image") or not profile.image:
            return "https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg"

        return profile.image.url

    def create(self, validated_data):
        post = validated_data.pop('post')
        comment = Comment.objects.create(post=post, **validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    profile_id = serializers.ReadOnlyField(source='author.profile.id')
    profile_image = serializers.ReadOnlyField(source='author.profile.profile_picture.url')
    image = serializers.ImageField(required=False)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'description', 'image', 'author',
            'profile_id', 'profile_image',
            'likes_count', 'has_liked', 'like_id',
            'comments_count', 'created_at', 'is_owner'
        ]

    def get_likes_count(self, obj):
        return obj.post_likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_like_id(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            like = Like.objects.filter(user=user, post=obj).first()
            return like.id if like else None
        return None

    def get_has_liked(self, obj):
        try:
            request = self.context.get("request")
            return request and request.user.is_authenticated and obj.post_likes.filter(user=request.user).exists()
        except Exception as e:
            import logging
            logging.error(f"🔴 Error in get_has_liked: {str(e)}")
            return False

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and request.user == obj.author

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if hasattr(value, 'image'):
            if value.image.height > 4096:
                raise serializers.ValidationError('Image height > 4096px!')
            if value.image.width > 4096:
                raise serializers.ValidationError('Image width > 4096px!')
        return value


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
