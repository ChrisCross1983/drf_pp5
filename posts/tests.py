from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class CreatePostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        response = self.client.post('/api/profiles/login/', {
            "username": "testuser",
            "password": "password123"
        })
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.valid_post_data = {
            "title": "Need a sitter",
            "category": "search",
            "description": "Looking for a cat sitter for 2 weeks.",
        }

    def test_create_post_successful(self):
        response = self.client.post('/api/posts/create/', self.valid_post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, "Need a sitter")

    def test_create_post_unauthenticated(self):
        self.client.credentials()
        response = self.client.post('/api/posts/create/', self.valid_post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
