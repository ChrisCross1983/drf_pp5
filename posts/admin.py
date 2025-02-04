from django.contrib import admin
from .models import Post, Comment, SittingRequest, Notification

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SittingRequest)
admin.site.register(Notification)

