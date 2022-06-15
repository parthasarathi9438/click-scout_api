from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user import views
from rest_framework.authtoken import views as auv
from rest_framework_simplejwt import views as jwtview

router = routers.DefaultRouter()
router.register('signup', views.SignupViewSet)
# router.register('login', views.LoginViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/<pk>', views.LoginViewSet.as_view()),
    path('api-token-auth/', auv.obtain_auth_token),
    path('get_details/', views.UserDetailAPI.as_view()),
    path('loginjwt/', jwtview.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', jwtview.TokenRefreshView.as_view(), name='token_refresh'),
    path('registerjwt/', views.UserRegister.as_view(), name='registerjwt'),
]
