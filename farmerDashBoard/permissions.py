# permissions.py - Custom permissions for the farmer dashboard API

from rest_framework import permissions

class IsFarmer(permissions.BasePermission):
    """
    Custom permission to only allow farmers to access farmer-specific views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == 'FARMER'

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a resource to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.farmer == request.user