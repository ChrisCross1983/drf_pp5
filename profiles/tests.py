from django.test import TestCase
from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework.test import APIClient
from rest_framework import status

# Test for registration
class RegistrationTestCase(TestCase):
    def setUp(self):
        self.valid_user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
        }
        self.invalid_user_data = {
            "username": "testuser2",
            "email": "testuser@example.com",
            "password": "short",
        }

    def test_user_registration_creates_profile(self):
        response = self.client.post('/api/profiles/register/', self.valid_user_data)
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)

        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)

    def test_duplicate_email_fails(self):
        self.client.post('/api/profiles/register/', self.valid_user_data)

        response = self.client.post('/api/profiles/register/', self.invalid_user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_password_validation(self):
        response = self.client.post('/api/profiles/register/', self.invalid_user_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

# Tests for login
class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123"
        )
        self.client = APIClient()
        self.login_url = '/api/profiles/login/'

    def test_login_successful(self):
        data = {"username": "testuser", "password": "securepassword123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failed(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials"
        )
