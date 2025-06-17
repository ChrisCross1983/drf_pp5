from rest_framework import serializers
from .models import Post, SittingRequest, SittingResponseMessage
from comments.models import Comment
from likes.models import Like
from profiles.serializers import ProfileMiniSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_profile = ProfileMiniSerializer(source='author.profile', read_only=True)
    image = serializers.ImageField(required=False)
    description = serializers.CharField(max_length=1000)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'description', 'image', 'author',
            'author_profile', 'likes_count', 'has_liked', 'like_id',
            'comments_count', 'created_at', 'updated_at', 'is_owner'
        ]

    def get_likes_count(self, obj):
        return obj.post_likes.count()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_like_id(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            like = Like.objects.filter(owner=user, post=obj).first()
            return like.id if like else None
        return None

    def get_has_liked(self, obj):
        request = self.context.get("request")
        return request and request.user.is_authenticated and obj.post_likes.filter(owner=request.user).exists()

    def get_is_owner(self, obj):
        request = self.context.get("request")
        return request and request.user == obj.author

    def validate_image(self, value):
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('Image is too large! Maximum allowed size is 10 MB.')
        if hasattr(value, 'image'):
            if value.image.height > 4096:
                raise serializers.ValidationError('Image height exceeds 4096px limit.')
            if value.image.width > 4096:
                raise serializers.ValidationError('Image width exceeds 4096px limit.')
        return value


class SittingRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    sender_profile_picture = serializers.SerializerMethodField()
    receiver_profile_picture = serializers.SerializerMethodField()
    message = serializers.CharField(
        max_length=500,
        allow_blank=True,
        allow_null=True,
        help_text="Optional message to include with the request."
    )

    class Meta:
        model = SittingRequest
        fields = [
            'id', 'sender', 'receiver', 'post', 'message', 'status',
            'created_at', 'sender_username', 'receiver_username', 'post_title',
            'sender_profile_picture', 'receiver_profile_picture',
        ]
        read_only_fields = ['id', 'sender', 'receiver', 'created_at']

    def get_sender_profile_picture(self, obj):
        profile = getattr(obj.sender, "profile", None)
        if profile and profile.profile_picture:
            return profile.profile_picture.url
        return "https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg"

    def get_receiver_profile_picture(self, obj):
        profile = getattr(obj.receiver, "profile", None)
        if profile and profile.profile_picture:
            return profile.profile_picture.url
        return "https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg"

    def create(self, validated_data):
        request = self.context.get("request")
        sender = validated_data.pop("sender", request.user)
        post = validated_data.pop("post", None)
        receiver = validated_data.pop("receiver", None) or post.author

        if not post:
            raise serializers.ValidationError("Post is required.")

        # Same user
        if post.author == request.user:
            raise serializers.ValidationError("You can't request your own post.")

        # Wrong category
        if post.category not in ["offer", "search"]:
            raise serializers.ValidationError("Sitting requests are only allowed for 'offer' or 'search' posts.")

        # Request already active
        if SittingRequest.objects.filter(sender=request.user, post=post).exists():
            raise serializers.ValidationError("You have already sent a request for this post.")

        # All checked
        sitting_request = SittingRequest.objects.create(
            sender=request.user,
            receiver=receiver or post.author,
            post=post,
            **validated_data
        )
        return sitting_request


class SittingResponseMessageSerializer(serializers.ModelSerializer):
    sender = ProfileMiniSerializer(source='sender.profile', read_only=True)
    content = serializers.CharField(
        max_length=500,
        help_text="Message content for the response."
    )

    class Meta:
        model = SittingResponseMessage
        fields = [
            'id',
            'sitting_request',
            'sender',
            'content',
            'created_at',
        ]
        read_only_fields = ['id', 'sender', 'created_at']

    def get_sender_profile_image(self, obj):
        profile = getattr(obj.sender, "profile", None)
        if profile and hasattr(profile, "profile_picture") and profile.profile_picture:
            return profile.profile_picture.url
        return "https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg"
