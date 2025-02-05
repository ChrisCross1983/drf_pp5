from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
import notifications.models

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
    description = models.TextField()
    image = CloudinaryField(
        'image', 
        blank=True, 
        null=True, 
        default='https://res.cloudinary.com/daj7vkzdw/image/upload/v1737570695/default_post_tuonop.jpg'
    )
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

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
