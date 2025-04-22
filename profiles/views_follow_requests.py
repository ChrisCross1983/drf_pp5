from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Profile, FollowRequest
from notifications.models import Notification

class FollowRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        receiver = get_object_or_404(Profile, pk=pk)
        sender = request.user.profile

        if receiver == sender:
            return Response({"error": "You cannot follow yourself."}, status=400)

        if FollowRequest.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({"error": "Follow request already sent."}, status=400)

        FollowRequest.objects.create(sender=sender, receiver=receiver)

        Notification.objects.create(
            user=receiver.user,
            type="follow",
            message=f"{request.user.username} sent you a follow request."
        )

        return Response({"message": "Follow request sent."}, status=201)


class FollowRequestRespondView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        action = request.data.get("action")
        follow_request = get_object_or_404(FollowRequest, id=request_id, receiver=request.user.profile)

        if action == "accept":
            follow_request.receiver.followers.add(follow_request.sender)
            follow_request.status = "accepted"
            follow_request.save()
            return Response({"message": "Follow request accepted."})

        elif action == "decline":
            follow_request.status = "declined"
            follow_request.save()
            return Response({"message": "Follow request declined."})

        return Response({"error": "Invalid action."}, status=400)


class FollowRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        sent = FollowRequest.objects.filter(sender=user)
        received = FollowRequest.objects.filter(receiver=user)

        return Response({
            "sent": [
                {
                    "id": r.id,
                    "to": r.receiver.user.username,
                    "status": r.status,
                    "created_at": r.created_at
                } for r in sent
            ],
            "received": [
                {
                    "id": r.id,
                    "from": r.sender.user.username,
                    "status": r.status,
                    "created_at": r.created_at
                } for r in received
            ]
        })


class FollowRequestCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, request_id):
        follow_request = get_object_or_404(FollowRequest, id=request_id, sender=request.user.profile)
        follow_request.delete()
        return Response({"message": "Follow request canceled."}, status=204)
