from django.urls import path, re_path
from .views import *
from . import views

urlpatterns=[
    path('api/user/register/', views.RegisterApiView.as_view(), name="register-user"),
    path('api/user/login/', views.LoginUser.as_view(), name="login-user"),
    path('api/auth-user/', views.UserView.as_view(), name="user-authenticated"),
]