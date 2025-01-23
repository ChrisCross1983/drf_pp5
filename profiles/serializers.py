from django.core.mail import send_mail
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture']

    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user, profile_picture=profile_picture)

        send_mail(
            'Welcome to Lucky Cat!',
            f'Hi {user.username}, thank you for registering on Lucky Cat!',
            'cborza83@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return user
