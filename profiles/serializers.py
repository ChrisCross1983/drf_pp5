from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    profile_picture = serializers.ImageField(required=False)
    location = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture', 'location']

    def create(self, validated_data):
        location = validated_data.pop('location', '')
        profile_picture = validated_data.pop('profile_picture', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user, location=location, profile_picture=profile_picture)
        return user
