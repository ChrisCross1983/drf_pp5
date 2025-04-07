# posts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SittingRequest
from comments.models import Comment
from notifications.models import Notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.author,
            message=f"{instance.owner.username} commented on your post."
        )


@receiver(post_save, sender=SittingRequest)
def create_sitting_request_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            type="request",
            sitting_request=instance,
            message=f"{instance.sender.username} sent you a sitting request."
        )
