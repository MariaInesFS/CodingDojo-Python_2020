from django.db import models

# Create your models here.
from django.db import models
import re

class UserManager(models.Manager):
    def basic_val(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last Name should be at least 3 characters"
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 6:
            errors['password']= "Password must be at least 6 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_pw'] = "Password doesn't match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Property(models.Model):
    PROPERTY_CHOICES = (
        ("apartment","Apartment"),
        ("house","House"),
        ("studio","Studio"),
        ("office","Office"),
        ("warehouse","Warehouse")
    )
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    price = models.IntegerField()
    property_type = models.CharField(max_length=80, choices=PROPERTY_CHOICES, default='studio')
    n_bedrooms= models.IntegerField(default=0)
    n_bathrooms = models.IntegerField(default=0)
    location = models.CharField(max_length=250)
    prop_image = models.ImageField(upload_to='uploaded_files/', default='image.jpg')
    landlord = models.ForeignKey(User, related_name="landlords", on_delete = models.CASCADE)
    tenant= models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    content = models.CharField(max_length=600)
    poster = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    message = models.ForeignKey(Property, related_name="reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
