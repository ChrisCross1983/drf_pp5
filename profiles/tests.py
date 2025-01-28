from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from profiles.models import Profile

# Test for registration
class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
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
        client = APIClient()
        response = self.client.post('/api/profiles/register/', self.valid_user_data)
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(username="testuser")
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)

    def test_duplicate_email_fails(self):
        self.client.post('/api/profiles/register/', self.valid_user_data)

        response = self.client.post('/api/profiles/register/', {
            "username": "testuser2",
            "email": "testuser@example.com",
            "password": "securepassword123"
        })
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

#Test for Logout
class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        
        response = self.client.post("/api/auth/login/", {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.access_token = response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_logout_success(self):
        response = self.client.post("/api/auth/logout/")
        
        print("DEBUG: Logout Response Status Code:", response.status_code)
        print("DEBUG: Logout Response Data:", response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Logged out successfully."})

    def test_logout_without_authentication(self):
        self.client.credentials()
        response = self.client.post("/api/auth/logout/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Test for Password Reset
class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123"
        )
        self.password_reset_url = reverse('password_reset')

    def test_password_reset_email_sent(self):
        response = self.client.post(self.password_reset_url, {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('testuser@example.com', mail.outbox[0].to)

    def test_password_reset_invalid_email(self):
        response = self.client.post(self.password_reset_url, {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)

# Test for Edit Profile
class EditProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        response = self.client.post('/api/profiles/login/', {
            "username": "testuser",
            "password": "password123"
        })

        print("Login Response Status Code:", response.status_code)
        print("Login Response Data:", response.data)

        self.access_token = response.data.get('access')
        if not self.access_token:
            print("Error: No Access Token received")

    def test_edit_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.put('/api/profiles/edit/', {
            "bio": "Updated bio",
            "profile_picture": "https://example.com/new_image.jpg"
        })
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['bio'], "Updated bio")

# Test for Password Change
class ChangePasswordTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        response = self.client.post('/api/profiles/login/', {
            "username": "testuser",
            "password": "password123"
        })
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_change_password_success(self):
        response = self.client.post('/api/profiles/password-change/', {
            "old_password": "password123",
            "new_password1": "newsecurepassword123",
            "new_password2": "newsecurepassword123"
        })
        self.assertEqual(response.status_code, 302)

    def test_change_password_mismatch(self):
        response = self.client.post('/api/profiles/password-change/', {
            "old_password": "password123",
            "new_password1": "newpassword1",
            "new_password2": "newpassword2"
        })
        self.assertEqual(response.status_code, 302)
        print("Password Change Response Status Code:", response.status_code)
        print("Password Change Response Data:", response.url)

# Test Follow / Unfollow profiles
class FollowUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        response = self.client.post('/api/profiles/login/', {
            "username": "user1",
            "password": "password123"
        })
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_follow_user(self):
        response = self.client.post(f'/api/profiles/{self.user2.profile.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Followed successfully.')

    def test_unfollow_user(self):
        self.client.post(f'/api/profiles/{self.user2.profile.id}/follow/')
        response = self.client.post(f'/api/profiles/{self.user2.profile.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Unfollowed successfully.')

    def test_cannot_follow_self(self):
        response = self.client.post(f'/api/profiles/{self.user1.profile.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "You cannot follow yourself.")

# Test for calling followers / following lists

    def test_get_followers(self):
        self.client.post(f'/api/profiles/{self.user2.profile.id}/follow/')
        response = self.client.get(f'/api/profiles/{self.user2.profile.id}/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], "user1")

    def test_get_following(self):
        self.client.post(f'/api/profiles/{self.user2.profile.id}/follow/')
        response = self.client.get(f'/api/profiles/{self.user1.profile.id}/following/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], "user2")

# Test Top 5 Followers
class TopFollowedProfilesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.users = [
            User.objects.create_user(username=f'user{i}', password='password123') for i in range(1, 7)
        ]
        for user in self.users:
            user.profile.followers.add(*[u.profile for u in self.users[:3]])

    def test_top_followed_profiles(self):
        response = self.client.get('/api/profiles/top-followed/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['follower_count'], 3)
