# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from fs_users.filters import UserFilterSet
from fs_users.models import CustomUser
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
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


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = UserFilterSet


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
