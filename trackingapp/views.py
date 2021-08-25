from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from django.core.checks import messages
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.
class RegisterApiView(generics.CreateAPIView):
    serializer_class=SignUpSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            response={
                "data":{
                    "user":dict(user_data),
                    "status":"success",
                    "message":"User created successfully"
                }
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    # login user is a post request
    def post(self, request):
        username=request.data['username']
        password=request.data['password']

        # to derive the first user with the username
        user=User.objects.filter(username=username).first()

        if user is None:
            # if user is not found
            raise AuthenticationFailed('user not found')

        if not user.check_password(password):
            # to check if the password is correct
            raise AuthenticationFailed('Incorrect Password')

        return Response({
            "message":"success"
        })



