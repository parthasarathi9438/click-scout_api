from os import access
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from user import serializer
from user.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from user.serializer import UserCreateSerializer, UserLoginSerializer, UserRegisterSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class SignupViewSet(ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class LoginViewSet(RetrieveAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (permissions.AllowAny,)

  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.User.id)
    serializer = UserLoginSerializer(user)
    return Response(serializer.data)


class UserRegister(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # print(user)
            refresh = RefreshToken.for_user(user)
            # print(refresh)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
