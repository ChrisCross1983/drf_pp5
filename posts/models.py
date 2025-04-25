from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.apps import apps


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_posts'
    )
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=[
            ('offer', 'Offer Sitting'),
            ('search', 'Search Sitting'),
            ('general', 'General'),
        ]
    )
    image = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570695/default_post_tuonop.jpg'
    )
    description = models.TextField(blank=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class SittingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='sitting_requests')
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} for post {self.post.title}"

class SittingResponseMessage(models.Model):
    sitting_request = models.ForeignKey(SittingRequest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message by {self.sender.username} on Request {self.request.id}"
