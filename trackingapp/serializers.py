from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django import forms

class SignUpSerializer(serializers.ModelSerializer):
    # email attribute is an EmailField and that it is required and should be unique
    email=serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # passwords are required, it is a character Field and is write_only and should be valid
    password=serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2=serializers.CharField(write_only=True, required=True)

    class Meta:
        model=User
        # fields to create a new user
        fields=('username', "email", "password", "password2")
        # extra kwargs add extra validations. Set the fields to be required
        # extra_kwargs={
        #     'bio':{'required': True}
        # }

    # password fields must be the same. We can validate these fields with serializers validate(self, attrs) method
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields did not match"})

        return attrs

    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # bio=validated_data['bio']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        exclude=['successful', 'issuccessful']

class isAcceptedSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields=['successful']

# serializers to filter by successful applications
class SuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields="__all__"

# post request for applications
class PostSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppSuccessful
        fields=['application']

# create a serializer that patches the model at two weeks
class AppSuccessSerializer2(serializers.ModelSerializer):
    class Meta:
        model=AppSuccessful
        fields=['twoWeeks']

# create a serializer that patches the model at four weeks
class AppSuccessSerializer4(serializers.ModelSerializer):
    class Meta:
        model=AppSuccessful
        fields=['fourWeeks']

# create a serializer that patches the model at eight weeks
class AppSuccessSerializer8(serializers.ModelSerializer):
    class Meta:
        model=AppSuccessful
        fields=['eightWeeks']

# create a serializer that patches the model at the end o weeks
# class AppSuccess(serializers.ModelSerializer):
#     class Meta:
#         model=AppSuccessful
#         fields=['completed']

# # create a serializer that patches the model at the interview dates
class AppSuccessSerailizer(serializers.ModelSerializer):
    class Meta:
        model=AppSuccessful
        fields=['interviewDates']


