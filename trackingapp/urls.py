from django.urls import path, re_path
from .views import *
from . import views

urlpatterns=[
    path('api/user/register/', views.RegisterApiView.as_view(), name="register-user"),
    path('api/user/login/', views.LoginUser.as_view(), name="login-user"),
    path('api/auth-user/', views.UserView.as_view(), name="user-authenticated"),
    path('api/make-entry/', views.ApplicationView.as_view(), name="new-application-entry"),
    path('api/edit-entry/<pk>/', views.ApplicationDetails.as_view(), name="application-details"),
    path('api/all-successful/',GetAllApplications.as_view(), name="allsuccessful"),
    path('api/new-wishlist-entry/', NewWishListEntry.as_view(), name="new-wishlist-entry"),
    path('api/wishlist-entry/<pk>/', WishListEntryDetails.as_view(), name="one-wishlist"),
    path('api/all-interviews/', GetAllInterviews.as_view(), name="all-interviews"),
    path('api/interviews/', Interviews.as_view(), name="interviews"),
    path('api/get-one-interview/<pk>/', InterviewDetails.as_view(), name="one-interview"),
    path('api/new-offer/',OfferDetails.as_view(), name="new-offer"),
    path('api/logout/', views.LogoutView.as_view(), name="logout-user")
]