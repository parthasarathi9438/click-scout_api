from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user import views

router = routers.DefaultRouter()
router.register('signup', views.SignupViewSet)
# router.register('login', views.LoginViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/<pk>', views.LoginViewSet.as_view()),
]
