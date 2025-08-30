from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Permission to only allow owners of a task to access it.
    """
    def has_object_permission(self, request, view, obj):
        # obj is Task instance
        return obj.user_id == request.user.id

class IsAdminOrSelf(BasePermission):
    """
    For user endpoints: admin can do anything; users can access/modify their own record.
    List is allowed only for admin.
    """
    def has_permission(self, request, view):
        # If trying to list users, only allow staff/admin
        if view.action == "list":
            return request.user and request.user.is_authenticated and request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        # obj is User instance
        return request.user and (request.user.is_staff or obj.id == request.user.id)
