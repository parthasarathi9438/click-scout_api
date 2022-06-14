from django.shortcuts import render
from user.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from user.serializer import UserCreateSerializer, UserLoginSerializer
from rest_framework.generics import RetrieveAPIView


class SignupViewSet(ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class LoginViewSet(RetrieveAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)