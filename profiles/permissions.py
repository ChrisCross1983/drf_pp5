from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, 'owner', getattr(obj, 'author', None)) == request.user


class IsAuthenticated(BasePermission):
    """
    Permission that allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated