from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment
from posts.models import Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='owner.username')
    replies = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    content = serializers.CharField(max_length=500)

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'is_owner', 'profile_id', 'profile_image',
            'post', 'created_at', 'updated_at', 'content',
            'replies', 'replies_count', 'parent', 'likes_count', 'has_liked'
        ]

    def get_replies(self, obj):
        children = obj.replies.all().order_by("-created_at")
        return CommentSerializer(children, many=True, context=self.context).data

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_has_liked(self, obj):
        user = self.context.get("request").user
        return user.is_authenticated and user in obj.likes.all()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner if request and request.user.is_authenticated else False

    def get_profile_image(self, obj):
        if hasattr(obj.owner, "profile") and obj.owner.profile.profile_picture:
            url = obj.owner.profile.profile_picture.url
            if not url.startswith("http"):
                return f"https://res.cloudinary.com/daj7vkzdw/{url}"
            return url
        return "https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg"

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data["owner"] = request.user
        return super().create(validated_data)


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model used in Detail view.
    Post is a read-only field so that we don’t have to set it on each update.
    """
    post = serializers.ReadOnlyField(source='post.id')
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields
