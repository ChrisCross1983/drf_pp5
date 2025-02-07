from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    TYPE_CHOICES = [
        ('request', 'Sitting Request'),
        ('comment', 'Comment'),
        ('like', 'Like'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='comment')
    sitting_request = models.ForeignKey(
        'posts.SittingRequest', on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"
