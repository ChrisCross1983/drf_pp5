"""
URL configuration for catsitting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for catsitting project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.middleware.csrf import get_token
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
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 🔹 Django Admin
    path('admin/', admin.site.urls),

    # 🔹 CSRF Token Endpoint (Wichtig für Frontend!)
    path("api/auth/csrf/", csrf_token_view, name="csrf-token"),

    # 🔹 Authentication Endpoints (dj-rest-auth)
    path('api/auth/login/', LoginView.as_view(), name='rest_login'),
    path('api/auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('api/auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('api/auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # 🔹 Profiles & Posts API Routes
    path('api/profiles/', include('profiles.urls')),
    path('api/posts/', include('posts.urls')),

    # 🔹 API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
