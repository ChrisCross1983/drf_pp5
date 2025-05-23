from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from comments.models import Comment
from comments.serializers import CommentSerializer
from .serializers import NotificationSerializer
from posts.models import Post


class DashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Unread notifications (max. 3)
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:3]
        notifications_data = NotificationSerializer(notifications, many=True).data

        # Newest comments to own post (max. 3)
        own_posts = Post.objects.filter(author=request.user)
        comments = Comment.objects.filter(post__in=own_posts).order_by('-created_at')[:3]

        # Additional fields on top
        comments_data = [
            {
                "id": c.id,
                "content": c.content,
                "created_at": c.created_at,
                "post_id": c.post.id,
                "post_title": c.post.title
            }
            for c in comments
        ]

        return Response({
            "notifications": notifications_data,
            "comments": comments_data
        })


class AllNotificationsView(ListAPIView):
    """
    API View to return all notifications for the logged-in user, sorted by created_at.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class MarkNotificationReadView(APIView):
    """
    API View to mark a specific notification as read.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(pk=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'message': 'Notification marked as read.'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)


class DashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Unread notifications (max. 3)
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:3]
        notifications_data = NotificationSerializer(notifications, many=True).data

        # Newest comments to own post (max. 3)
        own_posts = Post.objects.filter(author=request.user)
        comments = Comment.objects.filter(post__in=own_posts).order_by('-created_at')[:3]

        # Additional fields on top
        comments_data = [
            {
                "id": c.id,
                "content": c.content,
                "created_at": c.created_at,
                "post_id": c.post.id,
                "post_title": c.post.title
            }
            for c in comments
        ]

        return Response({
            "notifications": notifications_data,
            "comments": comments_data
        })


class AllNotificationsView(ListAPIView):
    """
    API View to return all notifications for the logged-in user, sorted by created_at.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class MarkNotificationReadView(APIView):
    """
    API View to mark a specific notification as read.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(pk=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'message': 'Notification marked as read.'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found.'}, status=status.HTTP_404_NOT_FOUND)


class MarkAllNotificationsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return Response({'message': 'All notifications marked as read.'}, status=status.HTTP_200_OK)
