from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from django.db.models.signals import post_delete
from django.dispatch import receiver
from notifications.models import Notification


class Comment(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.owner.username} on {self.post.title}"


@receiver(post_delete, sender=Comment)
def delete_related_notification(sender, instance, **kwargs):
    Notification.objects.filter(post=instance.post, type="comment").delete()
