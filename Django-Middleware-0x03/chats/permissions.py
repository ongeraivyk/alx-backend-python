from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to allow only owners to access their objects.
    """

    def has_object_permission(self, request, view, obj):
        # For Message model
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        # For Conversation model
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False
