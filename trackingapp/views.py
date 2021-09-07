from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from django.core.checks import messages
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.http import Http404

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

class ApplicationView(APIView):
    serializer_class=ApplicationSerializer

    # post a new application to database
    def post(self, request, format=None):
        serializers=self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            applications=serializers.data

            response={
                "data":{
                    "new_entry":dict(applications),
                    "status":"Success",
                    "message":"New entry made successfully"
                }
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    # get all application entries
    def get(self, request, format=None):
        applications=Application.objects.all()
        serializers=ApplicationSerializer(applications, many=True)
        return Response(serializers.data)

class ApplicationDetails(APIView):
    def get_application(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except:
            return Http404

    def get(self, request, pk, format=None):
        application=self.get_application(pk)
        serializers=ApplicationSerializer(application)
        return Response(serializers.data)

    # put request to update an existing application
    def put(self, request, pk, format=None):
        application=self.get_application(pk=pk)
        serializers=ApplicationSerializer(application, request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        application=self.get_application(pk)
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AcceptedDetails(generics.CreateAPIView):
    serializer_class=isAcceptedSerializer

    def patch(self, request, pk, format=None):
        app=Application.objects.get(pk=pk)

        serializers=isAcceptedSerializer(app, request.data, partial=True)

        if serializers.is_valid(raise_exception=True):
            serializers.save(successful=True)
            unsuccessful=serializers.data

            return Response(unsuccessful)
        return Response(status.errors, status=status.HTTP_400_BAD_REQUEST)

# get all applications where the applications are masked as successful
class GetAllApplications(APIView):
    serializer_class=SuccessSerializer

    def get(self, request, format=True):
        apps=Application.objects.filter(successful=True)
        serializers=self.serializer_class(apps, many=True)
        return Response(serializers.data)

# post on the app successful model
class AppSuccessful(generics.CreateAPIView):
    serializer_class=PostSuccessSerializer

    def post(self, request, pk, format=None):
        app=Application.objects.get(pk=pk)
        serializers=self.serializer_class(data=request.data)

        if serializers.is_valid(raise_exception=True):
            app.successful=True
            app.save()
            serializers.save() 
            app_data=serializers.data

            response={
                "data":dict(app_data),
                "status":"success",
                "message":"Application made successfully"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class AppSuccess2(generics.CreateAPIView):
    serializer_class=AppSuccessSerializer2

    def patch(self, request, pk, format=None):
        app=Application.objects.get(pk=pk)

        serializers=AppSuccessSerializer2(app,request.data, partial=True)

        if serializers.is_valid(raise_exception=True):
            serializers.save(twoWeeks=True)

            return Response(serializers.data)
        return Response(status.errors, status=status.HTTP_400_BAD_REQUEST)

