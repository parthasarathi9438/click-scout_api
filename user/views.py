from os import access
from django.shortcuts import render
from rest_framework.response import Response
from user.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from user.serializer import UserCreateSerializer, UserLoginSerializerAPI, ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate


class SignupViewSet(ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

class LoginAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializerAPI

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = request.user.email
        # print(email)
        user = authenticate(request, email=email, password=serializer.data['current_password'])
        if user is None:
            return Response({"message": "Incorrect details"}, status=status.HTTP_401_UNAUTHORIZED)
        request.user.set_password(serializer.data['new_password'])
        request.user.save()
        return Response({"message": "Successfully changed password"})