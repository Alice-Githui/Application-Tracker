from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
#     name=models.CharField(max_length=300)
#     email=models.EmailField(unique=True)
#     bio=models.CharField(max_length=300)
#     password=models.CharField(max_length=255, default="")

#     def __str__(self):
#         return self.name
        

class Application(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    companyName=models.CharField(max_length=500)
    jobTitle=models.CharField(max_length=500)
    description=models.CharField(max_length=800)

    def __str__(self):
        return self.companyName

class isAccepted(models.Model):
    application=models.OneToOneField(Application, on_delete=models.CASCADE)
    success=models.BooleanField(default=False)
    unsuccessful=models.BooleanField(default=False)

    def __str__(self):
        return str(self.application)

class AppSuccessful(models.Model):
    application=models.ForeignKey(Application, on_delete=models.CASCADE)
    twoWeeks=models.BooleanField(default=False)
    fourWeeks=models.BooleanField(default=False)
    eightWeeks=models.BooleanField(default=False)
    completed=models.BooleanField(default=False)
    interviewDates=models.CharField(max_length=300)

    def __str__(self):
        return str(self.application)

