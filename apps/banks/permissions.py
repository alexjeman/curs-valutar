from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrReadOnly(BasePermission):
    """The request is authenticated as a staff, or is a read-only request."""

    def has_permission(self, request, view):
        has_permission = bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )

        return has_permission
