from rest_framework import viewsets, permissions
from .models import SittingResponseMessage
from .serializers import SittingResponseMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class SittingResponseMessageViewSet(viewsets.ModelViewSet):
    queryset = SittingResponseMessage.objects.all().order_by("-created_at")
    serializer_class = SittingResponseMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("👤 Request user:", self.request.user)
        print("🔒 Authenticated:", self.request.user.is_authenticated)

        sitting_request = serializer.validated_data["sitting_request"]
        message = serializer.validated_data["message"]

        serializer.save(
            sender=self.request.user,
            receiver=sitting_request.receiver,
            sitting_request=sitting_request,
            message=message
        )

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
