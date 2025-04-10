# posts/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from .models import Post, SittingRequest
from comments.models import Comment
from notifications.models import Notification


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.post.author,
            type="comment",
            post=instance.post,
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

@receiver(post_delete, sender=Post)
def delete_post_notifications(sender, instance, **kwargs):
    Notification = apps.get_model('notifications', 'Notification')
    Notification.objects.filter(post=instance).delete()


@receiver(post_delete, sender=SittingRequest)
def delete_sitting_request_notifications(sender, instance, **kwargs):
    Notification = apps.get_model('notifications', 'Notification')
    Notification.objects.filter(sitting_request=instance).delete()
