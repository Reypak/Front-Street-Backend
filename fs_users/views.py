# views.py

from rest_framework.exceptions import PermissionDenied
# from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from fs_users.filters import UserFilterSet
from fs_users.models import CustomUser
from fs_utils.notifications.emails import send_templated_email
from fs_utils.utils import get_public_user_role
from .serializers import UserSerializer

import random
import string


def generate_random_password():
    length = 6
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))


def create_user_and_send_password_email(email, first_name=None, last_name=None, phone_number=None, role=None):
    password = generate_random_password()
    user = CustomUser.objects.create_user(
        email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, role=role)

    # Sending email
    subject = 'Your account details'
    context = {'user': user, 'password': password}

    send_templated_email(subject, 'account_creation.html',
                         context, [email])

    return user


class CreateUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            phone_number = serializer.validated_data.get('phone_number')
            role = serializer.validated_data.get(
                'role', get_public_user_role())

            user = create_user_and_send_password_email(
                email, first_name=first_name, last_name=last_name, phone_number=phone_number, role=role)

            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomPermission(BasePermission):
#     def has_permission(self, request, view):

#         return request.user.has_perm('roles.can_admin')

#     def has_object_permission(self, request, view, obj):

#         if 'role' in request.data and not request.user.has_perm('roles.can_admin'):
#             raise PermissionDenied(
#                 "You do not have permission to update role.")
#         return True

class IsStaffOrReadOnly(BasePermission):
    """
    Allows staff users to perform any action,
    and read-only actions for non-staff users.
    """

    def has_permission(self, request, view):
        # Allow any request if user is staff
        can_admin = request.user.role.permissions.filter(
            codename='can_admin').exists()
        if request.user and can_admin:
            return True

        # Non-staff users can only GET
        return request.method in ['GET', 'OPTIONS']

    def has_object_permission(self, request, view, obj):
        # Allow any request if user is staff
        can_admin = request.user.role.permissions.filter(
            codename='can_admin').exists()
        if request.user and can_admin:
            return True

        # Non-staff users can only read
        return request.method in ['GET', 'OPTIONS']


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilterSet


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrReadOnly]
