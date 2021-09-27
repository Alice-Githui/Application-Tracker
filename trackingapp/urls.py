from django.urls import path, re_path
from .views import *
from . import views

urlpatterns=[
    path('api/user/register/', views.RegisterApiView.as_view(), name="register-user"),
    path('api/user/login/', views.LoginUser.as_view(), name="login-user"),
    path('api/auth-user/', views.UserView.as_view(), name="user-authenticated"),
    path('api/make-entry/', views.ApplicationView.as_view(), name="new-application-entry"),
    path('api/edit-entry/<pk>/', views.ApplicationDetails.as_view(), name="application-details"),
    path('api/unsuccessful-entry/<pk>/', views.AcceptedDetails.as_view(), name="unsuccessful"),
    path('api/all-successful/',GetAllApplications.as_view(), name="allsuccessful"),
    path('api/logout/', views.LogoutView.as_view(), name="logout-user")
]