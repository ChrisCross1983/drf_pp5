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
        request = self.context.get("request")
        
        print("📥 VALIDATED DATA:", validated_data)
        print("🧾 FILES IN REQUEST:", request.FILES)
        print("✅ CONTEXT:", self.context)

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

        EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            defaults={"verified": False, "primary": True}
        )

        print("📂 DEBUG: validated_data:", validated_data)
        print("📂 DEBUG: profile_picture in validated_data?", "profile_picture" in validated_data)
        print("📂 DEBUG: profile_picture in FILES?", "profile_picture" in request.FILES)
        if "profile_picture" in request.FILES:
            print("📷 FILE NAME:", request.FILES["profile_picture"].name)
            print("📷 FILE TYPE:", request.FILES["profile_picture"].content_type)
            user.profile.profile_picture = request.FILES["profile_picture"]
            user.profile.save()
        else:
            print("⚠️ No profile_picture found in request.FILES")

        user.refresh_from_db()
        print("✅ Created User:", user.first_name, user.last_name)

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
    profile_picture = serializers.SerializerMethodField()
    total_posts = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return "https://res.cloudinary.com/daj7vkzdw/image/upload/v1744729686/Placeholder/hshdlbr977dc6dq9gt2o.jpg"

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
        print("🛠️ Incoming validated data:", validated_data)
        print("📂 Uploaded files:", self.context["request"].FILES)

        profile_pic = validated_data.pop("profile_picture", None)
        if profile_pic:
            instance.profile_picture = profile_pic
            print(f"✅ Profile picture uploaded: {instance.profile_picture}")

        instance.save()
        
        request = self.context.get("request")
        if request:
            user = instance.user
            first = request.data.get("first_name")
            last = request.data.get("last_name")
            
            if first is not None:
                user.first_name = first.strip()
            if last is not None:
                user.last_name = last.strip()

            user.save()

            print("✅ Updated User:", user.first_name, user.last_name)

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
