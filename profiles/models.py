from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')  # Hier ersetzt
    bio = models.TextField(blank=True, null=True)
    profile_picture = CloudinaryField(
        'image', 
        default='https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570810/default_profile_uehpos.jpg'
    )
    followers = models.ManyToManyField("self", symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s profile"
