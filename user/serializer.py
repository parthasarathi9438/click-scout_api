from dataclasses import fields
from pyexpat import model
from venv import create
from rest_framework import serializers
from user.models import User
from rest_framework.authtoken.models import Token
from django.db.models import Q


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirmed', 'is_staff', 'is_superuser', 'is_active')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
            confirmed=validated_data.get('confirmed'),
            is_staff=validated_data.get('is_staff'),
            is_superuser=validated_data.get('is_superuser'),
            is_active=validated_data.get('is_active'),
        )
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=8, write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirmed', 'is_staff', 'is_superuser', 'is_active',)
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
            confirmed=validated_data.get('confirmed'),
            is_staff=validated_data.get('is_staff'),
            is_superuser=validated_data.get('is_superuser'),
            is_active=validated_data.get('is_active')
        )
        user.save()
        return user


class KnoxRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])
        return user

class KnoxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class UserLoginSerializerAPI(serializers.ModelSerializer):
    username = serializers.CharField(required=False,allow_blank=True,write_only=True,)
    email = serializers.EmailField(required=False,allow_blank=True,write_only=True,label="Email Address")
    token = serializers.CharField(allow_blank=True,read_only=True)
    password = serializers.CharField(required=True,write_only=True,style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if not email and not username:
            raise serializers.ValidationError("enter username or email to login.")
        user = User.objects.filter(Q(email=email) | Q(username=username)).exclude(email__isnull=True).exclude(email__iexact='').distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("not valid.")
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")
        if user_obj.is_active:
            token, create = Token.objects.get_or_create(user=user_obj)
            data['token'] = token
        else:
            raise serializers.ValidationError("User not active.")
        return data