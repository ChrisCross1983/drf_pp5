from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = CloudinaryField(
        'image',
        default='https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg'
    )
    followers = models.ManyToManyField("self", symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    elif not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)

class FollowRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
    ]

    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sent_follow_requests")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="received_follow_requests")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")
        ordering = ["-created_at"]

    def __str__(self):
        from_user = getattr(self.sender.user, "username", "unknown")
        to_user = getattr(self.receiver.user, "username", "unknown")
        return f"FollowRequest from {from_user} to {to_user} ({self.status})"
