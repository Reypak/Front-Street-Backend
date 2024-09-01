# from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from fs_utils.constants import CAN_ADMIN

# class CustomPermission(BasePermission):
#     def has_permission(self, request, view):

#         return request.user.has_perm('roles.can_admin')

#     def has_object_permission(self, request, view, obj):

#         if 'role' in request.data and not request.user.has_perm('roles.can_admin'):
#             raise PermissionDenied(
#                 "You do not have permission to update role.")
#         return True


class IsAuthenticatedStaff(BasePermission):
    def has_permission(self, request, view):

        has_staff_fields = 'role' not in request.data
        # and 'is_staff' not in request.data

        # Allow any request, but with restrictions
        if not request.user.is_authenticated:
            return has_staff_fields

        has_permissions = request.user.role.permissions.filter(
            codename=CAN_ADMIN).exists()

        # Authenticated user with permissions
        if has_permissions:
            return True

        # Authenticated without permissions
        if request.user.is_authenticated:
            return has_staff_fields


class IsStaffOrReadOnly(BasePermission):
    """
    Allows staff users to perform any action,
    and read-only actions for non-staff users.
    """

    def has_permission(self, request, view):
        # Allow any request if user is staff
        can_admin = request.user.role.permissions.filter(
            codename=CAN_ADMIN).exists()
        if request.user and can_admin:
            return True

        # Non-staff users can only GET
        return request.method in ['GET', 'OPTIONS']

    def has_object_permission(self, request, view, obj):
        # Allow any request if user is staff
        can_admin = request.user.role.permissions.filter(
            codename=CAN_ADMIN).exists()
        if request.user and can_admin:
            return True

        # Non-staff users can only read
        return request.method in ['GET', 'OPTIONS']
