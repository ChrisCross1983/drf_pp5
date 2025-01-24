from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import Profile
from .serializers import ProfileSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly

class RegisterView(CreateAPIView):
    """
    Endpoint to register a new user.
    """
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CurrentUserProfileView(APIView):
    """
    Endpoint to retrieve the profile of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class UserProfileView(RetrieveAPIView):
    """
    Endpoint to retrieve the profile of a specific user by ID.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

class EditProfileView(RetrieveUpdateAPIView):
    """
    Endpoint to allow users to edit their profile details.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')
    permission_classes = [IsAuthenticated] 