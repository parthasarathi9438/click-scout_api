from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from user.manager import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=127, blank=True)
    first_name = models.CharField(max_length=127, blank=True)
    last_name = models.CharField(max_length=127, blank=True)
    email = models.EmailField(unique=True)
    confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email
