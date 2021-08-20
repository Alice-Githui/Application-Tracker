from django.urls import path, re_path
from .views import *
from . import views

urlpatterns=[
    path('api/user/register/', views.RegisterApiView.as_view(), name="register-user"),
]