from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment
from posts.models import Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'is_owner', 'profile_id', 'profile_image',
            'post', 'created_at', 'updated_at', 'content'
        ]

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner if request and request.user.is_authenticated else False

    def get_profile_image(self, obj):
        profile = getattr(obj.owner, "profile", None)
        if not profile or not getattr(profile, "image", None):
            return "https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg"
        return profile.image.url

    def create(self, validated_data):
        post = validated_data.pop('post')
        return Comment.objects.create(post=post, **validated_data)


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model used in Detail view.
    Post is a read-only field so that we don’t have to set it on each update.
    """
    post = serializers.ReadOnlyField(source='post.id')
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields
