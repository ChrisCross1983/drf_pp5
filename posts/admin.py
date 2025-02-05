from django.contrib import admin
from .models import Post, Comment, SittingRequest
import notifications.models

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SittingRequest)
admin.site.register(notifications.models.Notification)
