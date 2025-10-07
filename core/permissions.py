from rest_framework.permissions import BasePermission

class IsAnalystOrReadOnly(BasePermission):
    """
    Allow write for users flagged as analysts. Read for others.
    """
    def has_permission(self, request, view):
        if request.method in ("GET","HEAD","OPTIONS"):
            return True
        user = request.user
        return bool(user and getattr(user, "is_authenticated", False) and getattr(user, "is_data_analyst", False))
