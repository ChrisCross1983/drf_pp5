from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from dj_rest_auth.registration.views import RegisterView
from profiles.views import CustomLoginView, CustomLogoutView
from likes import views as likes_views
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView

# CSRF-Token API View
def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

# API-Documentation with Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Catsitting API",
        default_version="v1",
        description="API documentation for Catsitting project",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # 🔹 Django Admin
    path('admin/', admin.site.urls),

    # 🔹 CSRF & JWT Token Endpoint
    path('api/auth/csrf/', csrf_token_view, name='csrf-token'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 Authentication Endpoints (dj-rest-auth)
    path('api/auth/login/', CustomLoginView.as_view(), name='rest_login'),
    path('api/auth/logout/', CustomLogoutView.as_view(), name='rest_logout'),
    path('api/auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('api/auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),

    # 🔹 Profiles, Posts & Notifications APIs
    path('api/profiles/', include('profiles.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/comments/', include('comments.urls')),

    # 🔹 API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
