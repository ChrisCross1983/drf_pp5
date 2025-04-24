from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Profile, FollowRequest
from notifications.models import Notification


class FollowRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, target_id):
        target_profile = get_object_or_404(Profile, pk=target_id)
        sender_profile = request.user.profile

        if sender_profile == target_profile:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        existing = FollowRequest.objects.filter(
            sender=sender_profile,
            receiver=target_profile
        ).first()

        print("📌 Existing follow request(s):", existing)

        if existing:
            if existing.status == "declined":
                existing.status = "pending"
                existing.save()
                print("🔄 Re-activated previously declined request")
            else:
                return Response(
                    {"detail": f"Follow request already active. Status: {existing.status}"},
                    status=400
                )
        else:
            follow_request = FollowRequest.objects.create(
                sender=sender_profile,
                receiver=target_profile
            )
            print("✅ FollowRequest created with ID:", follow_request.id)

        Notification.objects.create(
            user=target_profile.user,
            type="follow",
            message=f"{request.user.username} sent you a follow request.",
            sender_profile=request.user.profile
        )

        return Response({"detail": "Request sent successfully!"}, status=201)


class FollowRequestRespondView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        action = request.data.get("action")
        follow_request = get_object_or_404(FollowRequest, id=request_id, receiver=request.user.profile)

        if action == "accept":
            sender = follow_request.sender
            receiver = follow_request.receiver

            sender.following.add(receiver)

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
        user_profile = request.user.profile
        sent = FollowRequest.objects.filter(sender=user_profile, status="pending")
        received = FollowRequest.objects.filter(receiver=user_profile, status="pending")

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


class UnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, target_id):
        profile = get_object_or_404(Profile, pk=target_id)
        request.user.profile.following.remove(profile)
        
        FollowRequest.objects.filter(
            sender=request.user.profile,
            receiver=profile,
            status="accepted"
        ).delete()

        return Response({"message": "Unfollowed successfully."}, status=204)
