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

class WishList(models.Model):
    companyName=models.CharField(max_length=500)
    position=models.CharField(max_length=300)
    location=models.CharField(max_length=300)
    website=models.URLField(max_length=1000)

    def __str__(self):
        return self.companyName
        

class Application(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    companyName=models.CharField(max_length=500)
    jobTitle=models.CharField(max_length=500)
    description=models.CharField(max_length=800)


    def __str__(self):
        return self.companyName

class Interviews(models.Model):
    application=models.ForeignKey(Application, on_delete=models.CASCADE)
    date=models.DateTimeField()
    location=models.CharField(max_length=300)

    def __str__(self):
        return str(self.application.companyName)

