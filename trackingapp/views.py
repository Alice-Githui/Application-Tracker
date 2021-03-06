from django.shortcuts import get_object_or_404, render
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


# get all applications where the applications are masked as successful
class GetAllApplications(APIView):
    serializer_class=SuccessSerializer

    def get(self, request, format=True):
        apps=Application.objects.filter(successful=True)
        serializers=self.serializer_class(apps, many=True)
        return Response(serializers.data)

# API view to create a new wishlist entry
class NewWishListEntry(APIView):
    serializer_class=WishListSerializer

    def get(self, request, format=None):
        wishlist_entries=WishList.objects.all()
        serializers=self.serializer_class(wishlist_entries, many=True)
        return Response(serializers.data)

    def post(self, request, format=True):
        serializers=self.serializer_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            new_wishlist=serializers.data

            response={
                "data":{
                    "new_entry":dict(new_wishlist),
                    "status": "Success",
                    "message": "New entry has been made successfully"
                }
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# API View to get one specific wish entry
class WishListEntryDetails(APIView):
    serializer_class=WishListSerializer

    def get_wishlist(self, pk):
        try:
            return WishList.objects.get(pk=pk)
        except:
            return Http404

    def get(self, request, pk, format=None):
        wishlist=self.get_wishlist(pk)
        serializers=WishListSerializer(wishlist)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        wishlist=self.get_wishlist(pk=pk)
        serializers=WishListSerializer(wishlist, request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        wishlist=self.get_wishlist(pk)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Interviews(APIView):
    serializer_class=InterviewsSerializer

    def post(self, request, format=None):
    
        serializers=InterviewsSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            interview=serializers.data

            response={
                "data":{
                    "new_entry":dict(interview),
                    "status":"Success",
                    "message": "New Interview set successfully"
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllInterviews(APIView):
    serializer_class=InterviewsSerializer

    def get(self, request, format=None):
        interviews=Interview.objects.all()
        serializers=InterviewsSerializer(interviews, many=True)
        return Response(serializers.data)

class InterviewDetails(APIView):
    # get one interview
    def get_interviewdetails(self, pk):
        try:
            return Interview.objects.get(pk=pk)
        except:
            return Http404

    def get(self, request, pk, format=None):
        interview=self.get_interviewdetails(pk)
        serializers=InterviewsSerializer(interview)
        return Response(serializers.data)

    # put request for one interview
    def put(self, request, pk, format=None):
        interview=Interview.objects.get(pk=pk)
        serializers=InterviewsSerializer(interview, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        interview=Interview.objects.get(pk=pk)
        interview.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# API endpoint to post a new offer
class OfferDetails(APIView):
    serializer_class=OfferSerializer

    #  get all offers
    def get(self, request, format=None):
        received_offers=Offer.objects.all()
        serializers=self.serializer_class(received_offers, many=True)
        return Response(serializers.data)

    # post a new offer
    def post(self, request, format=None):
        serializers=OfferSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            offers=serializers.data

            response={
                "data":{
                    "new-entry":dict(offers),
                    "status":"Success",
                    "message": "New offer was made"
                }
            }

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class OneOfferDetail(APIView):
    serializer_class=OfferSerializer

    # get an offer using id
    def get_offer(self, pk):
        try:
            return Offer.objects.get(pk=pk)
        except:
            return Http404

    def get(self, request, pk, format=None):
        offer=self.get_offer(pk)
        serializers=OfferSerializer(offer)
        return Response(serializers.data)

    # get and amend details for one offer
    def put(self, request, pk, format=None):
        offer=Offer.objects.get(pk=pk)
        serializer=self.serializer_class(offer, request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an offer from the list of offers
    def delete(self, request, pk, format=None):
        offer=OfferSerializer.objects.get(pk=pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






