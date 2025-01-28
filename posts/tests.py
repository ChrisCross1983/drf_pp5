from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment, SittingRequest, Notification

# Test Create Post
class CreatePostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

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
        self.client.logout()
        response = self.client.post('/api/posts/create/', self.valid_post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Test Post Feed
class PostFeedTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        for i in range(15):
            Post.objects.create(
                author=self.user,
                title=f"Post {i}",
                category="general",
                description="This is a test post",
            )

    def test_feed_pagination(self):
        response = self.client.get('/api/posts/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

    def test_infinite_scrolling(self):
        response = self.client.get('/api/posts/feed/?page=1')
        self.assertEqual(len(response.data['results']), 10)

        response = self.client.get('/api/posts/feed/?page=2')
        self.assertEqual(len(response.data['results']), 5)

# Test Comment and Like
class PostInteractionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            category="general",
            description="This is a test post"
        )

    def test_like_post(self):
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.likes.count(), 1)

    def test_add_comment(self):
        data = {"content": "This is a test comment"}
        response = self.client.post(f'/api/posts/{self.post.id}/comment/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.comments.count(), 1)

# Test Search and Filter Options
class PostSearchFilterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        Post.objects.create(author=self.user, title="Offer Sitting", category="offer", description="Looking for a sitter")
        Post.objects.create(author=self.user, title="Search Sitting", category="search", description="Need a sitter")
        Post.objects.create(author=self.user, title="General Tips", category="general", description="Tips for cats")

    def test_search_posts(self):
        response = self.client.get('/api/posts/feed/?search=sitter')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_posts_by_category(self):
        response = self.client.get('/api/posts/feed/?category=offer')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

# Test Delete and Edit Post
class EditDeletePostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        self.post = Post.objects.create(
            author=self.user,
            title="Initial Title",
            category="general",
            description="Initial Description"
        )

    def test_edit_post(self):
        response = self.client.put(f'/api/posts/{self.post.id}/', {
            "title": "Updated Title",
            "category": "offer",
            "description": "Updated Description",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Updated Title")

    def test_delete_post(self):
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

# Test Edit / Delete Comments
class EditDeleteCommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.post = Post.objects.create(author=self.user, title="Test Post", category="general", description="Test description")
        self.comment = Comment.objects.create(author=self.user, post=self.post, content="Original comment")

        self.client.login(username="testuser", password="password123")

    def test_edit_comment(self):
        response = self.client.put(f'/api/posts/comments/{self.comment.id}/', {"content": "Updated comment"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], "Updated comment")

    def test_delete_comment(self):
        response = self.client.delete(f'/api/posts/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

# Test Sitting Requests
class SittingRequestTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        self.post = Post.objects.create(
            author=self.user2,
            title="Looking for a sitter",
            category="search",
            description="I need a sitter for my cat this weekend."
        )

        self.client.login(username="user1", password="password123")

    def test_create_sitting_request(self):
        response = self.client.post(f'/api/posts/{self.post.id}/request/', {"message": "I can help!"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SittingRequest.objects.count(), 1)

    def test_cannot_request_own_post(self):
        self.client.logout()
        self.client.login(username="user2", password="password123")

        response = self.client.post(f'/api/posts/{self.post.id}/request/', {"message": "I want to request my own post"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# Test Managing Sitting Requests
class SittingRequestManagementTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        self.post = Post.objects.create(
            author=self.user2,
            title="Looking for a sitter",
            category="search",
            description="I need a sitter for my cat this weekend."
        )

        self.sitting_request = SittingRequest.objects.create(
            sender=self.user1,
            receiver=self.user2,
            post=self.post,
            message="I can help with sitting!"
        )

        self.client.login(username="user2", password="password123")

    def test_incoming_requests(self):
        response = self.client.get('/api/posts/requests/incoming/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_manage_request_accept(self):
        response = self.client.post(f'/api/posts/requests/manage/{self.sitting_request.id}/', {"action": "accept"})
        self.assertEqual(response.status_code, 200)
        self.sitting_request.refresh_from_db()
        self.assertEqual(self.sitting_request.status, 'accepted')

    def test_manage_request_decline(self):
        response = self.client.post(f'/api/posts/requests/manage/{self.sitting_request.id}/', {"action": "decline"})
        self.assertEqual(response.status_code, 200)
        self.sitting_request.refresh_from_db()
        self.assertEqual(self.sitting_request.status, 'declined')

# Test Notifications
class NotificationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.client = APIClient()

        self.post = Post.objects.create(
            author=self.user1,
            title="Test Post",
            category="general",
            description="Test description"
        )

        self.client.login(username="user2", password="password123")

    def test_like_notification(self):
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user1)
        self.assertEqual(notification.type, 'like')