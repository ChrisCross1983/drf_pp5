from django.db import models
from django.conf import settings

class SittingResponse(models.Model):
    request = models.ForeignKey("posts.SittingRequest", on_delete=models.CASCADE, related_name="responses")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Response by {self.sender.username} for request {self.request.id}"
