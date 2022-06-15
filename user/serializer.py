from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from user.models import User


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