from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Profile
from posts.models import Post

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8, required=True)
    password2 = serializers.CharField(write_only=True, min_length=8, required=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2", "profile_picture"]

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Passwords must match."})
        return data

    def validate_email(self, value):
        existing_user = User.objects.filter(email=value).first()
        if existing_user:
            email_address = EmailAddress.objects.filter(user=existing_user, email=value).first()
            if email_address and email_address.verified:
                raise ValidationError("A user with this email already exists and is verified.")
        return value

    def create(self, validated_data):
        profile_picture = validated_data.pop("profile_picture", None)
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password1"],
            first_name=first_name,
            last_name=last_name,
        )

        email_address, created = EmailAddress.objects.get_or_create(
            user=user, email=user.email, defaults={"verified": False, "primary": True}
        )

        if profile_picture:
            user.profile.profile_picture = profile_picture
            user.profile.save()

        send_mail(
            "Welcome to Lucky Cat!",
            f"Hi {user.username}, thank you for registering on Lucky Cat!",
            "cborza83@gmail.com",
            [user.email],
            fail_silently=False,
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', allow_blank=True, required=False)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True, required=False)
    owner = serializers.ReadOnlyField(source='user.username')
    total_posts = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'first_name', 'last_name', 'bio', 'profile_picture',
            'total_posts', 'followers_count', 'following_count',
            'is_following', 'is_owner',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'owner', 'total_posts', 'followers_count',
            'following_count', 'is_following', 'is_owner',
            'created_at', 'updated_at'
        ]

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        profile_pic = validated_data.pop("profile_picture", None)
        if profile_pic:
            instance.profile_picture = profile_pic
            print(f"✅ Profile picture uploaded: {instance.profile_picture}")
        instance.save()
        
        user = instance.user
        request = self.context.get("request")
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.save()

        return instance

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.user if request and request.user.is_authenticated else False


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'description', 'image', 'author', 'created_at']
