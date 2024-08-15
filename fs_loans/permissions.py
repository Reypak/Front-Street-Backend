from rest_framework.permissions import BasePermission, SAFE_METHODS


class LoanPermission(BasePermission):
    """
    Custom permission to allow only staff to edit loans.
    Additionally, only users with a specific permission can update the 'status' field.
    """

    def has_permission(self, request, view):
        # Allow all read-only methods (e.g., GET, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Staff users can edit the loan (but not necessarily update the status field)
        if request.user.is_staff:
            return True

        # For non-staff, deny permission by default
        return False

    def has_object_permission(self, request, view, obj):
        # Staff can edit any field except 'status'
        if request.user.is_staff and 'status' not in request.data:
            return True

        # List of permission codenames required to change the status field
        required_permissions = ['can_admin', 'can_change_loan_status']

        # Check if the user has the specific permission to update the status field
        has_permissions = request.user.role.permissions.filter(
            codename__in=required_permissions).exists()

        if 'status' in request.data and has_permissions:
            return True

        # For all other cases, deny permission
        return False
