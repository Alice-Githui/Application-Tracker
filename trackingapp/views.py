from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from django.core.checks import messages
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

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

        payload={
            # user id to identify the user
            "id":user.id,
            # use datetime to define how long the token is valid. The token is valid for 60 minutes
            'exp':datetime.datetime.utcnow() +datetime.timedelta(minutes=60), 
            # date when the token is created
            'iat':datetime.datetime.utcnow()
        }

        token=jwt.encode(payload, 'secret', algorithm='HS256')

        response=Response()

        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data={
            'jwt':token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload=jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        # get the user using the payload id
        user=User.objects.filter(id=payload['id']).first()

        # return serialized info about the user
        serilaizer=SignUpSerializer(user)
        return Response(serilaizer.data)

class LogoutView(APIView):
    def post(self, request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':"Successfully logged out"
        }

        return response

