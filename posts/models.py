from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Post(models.Model):
    author = models.ForeignKey(
        User,
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
