from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile, CustomUser

User = get_user_model()

# Test for registration
class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "securepassword123",
        }
        self.invalid_user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "short",
        }

    def test_user_registration_creates_profile(self):
        response = self.client.post('/api/profiles/register/', self.valid_user_data, format="json")
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email="testuser@example.com")
        profile = Profile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)

    def test_duplicate_email_fails(self):
        self.client.post('/api/profiles/register/', self.valid_user_data, format="json")

        response = self.client.post('/api/profiles/register/', self.valid_user_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_password_validation(self):
        response = self.client.post('/api/profiles/register/', self.invalid_user_data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="securepassword123"
        )
        self.client = APIClient()
        self.login_url = '/api/auth/login/'

    def test_login_successful(self):
        data = {"email": "testuser@example.com", "password": "securepassword123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("key", response.data)

    def test_login_failed(self):
        data = {"email": "testuser@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

# Test for Logout
class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", username="testuser", password="password123")
        self.client.login(email="testuser@example.com", password="password123")

    def test_logout_success(self):
        response = self.client.post("/api/auth/logout/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "Successfully logged out."})

# Test for Password Reset
class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
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
        self.user = User.objects.create_user(email="testuser@example.com", username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(email="testuser@example.com", password="password123")

    def test_edit_profile(self):
        response = self.client.put('/api/profiles/edit/', {
            "bio": "Updated bio",
            "profile_picture": "https://example.com/new_image.jpg"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['bio'], "Updated bio")

# Test for Password Change
class ChangePasswordTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(email="testuser@example.com", password="password123")

    def test_change_password_success(self):
        response = self.client.post('/api/profiles/password-change/', {
            "old_password": "password123",
            "new_password1": "newsecurepassword123",
            "new_password2": "newsecurepassword123"
        }, format="json")
        self.assertEqual(response.status_code, 200)

    def test_change_password_mismatch(self):
        response = self.client.post('/api/profiles/password-change/', {
            "old_password": "password123",
            "new_password1": "newpassword1",
            "new_password2": "newpassword2"
        }, format="json")
        self.assertEqual(response.status_code, 200)

# Test Follow / Unfollow profiles
class FollowUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="user1@example.com", username="user1", password="password123")
        self.user2 = User.objects.create_user(email="user2@example.com", username="user2", password="password123")
        self.client.login(email="user1@example.com", password="password123")

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

# Test Top 5 Followers
class TopFollowedProfilesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.users = [
            CustomUser.objects.create_user(
                email=f'user{i}@example.com',
                username=f'user{i}',
                password='password123'
            ) for i in range(1, 7)
        ]

        for i, user in enumerate(self.users):
            followers = [u.profile for j, u in enumerate(self.users) if j != i][:5]
            user.profile.followers.add(*followers)

        for profile in Profile.objects.all():
            print(f"{profile.user.email} hat {profile.followers.count()} Follower")

    def test_top_followed_profiles(self):
        response = self.client.get('/api/profiles/top-followed/')
        self.assertEqual(response.status_code, 200)

        expected_count = min(5, len(self.users))
        actual_count = len(response.data)

        print("API Response Data:", response.data)
        print(f"Expected: {expected_count}, Actual: {actual_count}")

        self.assertEqual(actual_count, expected_count)
