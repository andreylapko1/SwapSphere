from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsReceiver(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.ad_receiver.user != request.user:
            raise PermissionDenied("You do not have permission to confirm this exchange.")
        return True