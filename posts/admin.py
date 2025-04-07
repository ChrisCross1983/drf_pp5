from django.contrib import admin
from .models import Post, SittingRequest
from comments.models import Comment
import notifications.models

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SittingRequest)
admin.site.register(notifications.models.Notification)
