from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=20)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    number = models.IntegerField(default=2)

class Detailed_desc(models.Model):
    dest_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=20)
    days = models.IntegerField(default=5)
    price = models.IntegerField(default=20000)
    rating = models.IntegerField(default=5)
    dest_name = models.CharField(max_length=25)
    img1=models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    desc = models.TextField()
    day1= models.CharField(max_length=200)
    day2 = models.CharField(max_length=200)
    day3 = models.CharField(max_length=200)
    day4 = models.CharField(max_length=200)
    day5 = models.CharField(max_length=200)
    day6 = models.CharField(max_length=200)

class pessanger_detail(models.Model):
    Trip_id = models.AutoField(primary_key=True)
    Trip_same_id = models.IntegerField(default=1)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    age = models.IntegerField(default=10)
    username = models.CharField(max_length=10)
    Trip_date = models.DateField()
    payment = models.IntegerField(default=50)
    city = models.CharField(max_length=20)
    pay_done = models.IntegerField(default=0)
