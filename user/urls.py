from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user import views
from rest_framework.authtoken import views as auv
from rest_framework_simplejwt import views as jwtview
from django.views.decorators.csrf import csrf_exempt

router = routers.DefaultRouter()
router.register('signup', views.SignupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth_token/', auv.obtain_auth_token),
    path('login_api/', views.LoginAPI.as_view(), name='login_api'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
