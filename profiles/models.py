from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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
