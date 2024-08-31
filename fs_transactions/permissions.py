from rest_framework.permissions import BasePermission

from fs_utils.constants import CAN_ADD_TRANSACTION, CAN_ADMIN, CAN_VIEW_TRANSACTION


class TransactionPermission(BasePermission):
    """
    Custom permission to allow only users with specific permissions to view or add transactions.
    """

    def has_permission(self, request, view):
        # Check for GET requests (view transactions)
        if request.method == 'GET':
            return request.user.role.permissions.filter(
                codename__in=[
                    CAN_ADMIN,
                    CAN_VIEW_TRANSACTION]).exists()

        # Check for POST requests (add transactions)
        if request.method == 'POST':
            return request.user.role.permissions.filter(
                codename__in=[
                    CAN_ADMIN,
                    CAN_ADD_TRANSACTION]).exists()

        # Deny permission for all other methods
        return False
