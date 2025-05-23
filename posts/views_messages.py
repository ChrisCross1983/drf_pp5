from rest_framework import viewsets, permissions
from .models import SittingResponseMessage
from .serializers import SittingResponseMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from notifications.models import Notification


class SittingResponseMessageViewSet(viewsets.ModelViewSet):
    queryset = SittingResponseMessage.objects.all().order_by("-created_at")
    serializer_class = SittingResponseMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        sitting_request = serializer.validated_data["sitting_request"]
        content = serializer.validated_data["content"]

        message = serializer.save(
            sender=self.request.user,
            sitting_request=sitting_request,
            content=content
        )

        Notification.objects.create(
            user=sitting_request.receiver if self.request.user == sitting_request.sender else sitting_request.sender,
            type="sitting_message",
            sitting_request=sitting_request,
            message=f"New message on your sitting request for post '{sitting_request.post.title}'"
        )

        return message

    def get_queryset(self):
        """
        Only show messages related to sitting requests where the user is sender or receiver.
        """
        user = self.request.user
        return SittingResponseMessage.objects.filter(
            sitting_request__sender=user
        ) | SittingResponseMessage.objects.filter(
            sitting_request__receiver=user
        )
