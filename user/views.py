from os import access
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from user import serializer
from user.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from user.serializer import UserCreateSerializer, UserLoginSerializer, UserRegisterSerializer, KnoxUserSerializer,\
     KnoxRegisterSerializer, UserLoginSerializerAPI, ChangePasswordSerializer
from rest_framework.generics import RetrieveAPIView, GenericAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from knox.models import AuthToken
from knox.views import LoginView
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


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


class KnoxRegister(GenericAPIView):
    serializer_class = KnoxRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # print(user)
        return Response({
        "user": KnoxUserSerializer(user).data,
        "token": AuthToken.objects.create(user)[1]
        })

class KnoxLogin(LoginView):
    permission_classes = (permissions.IsAuthenticated,)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(KnoxLogin, self).post(request, format=None)

class LoginAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializerAPI

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ChangePassword(UpdateAPIView):
#     serializer_class = UserPasswordSerializer
#     queryset = User.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }
#             return Response(response)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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