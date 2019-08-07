from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                              CASCADE)
from django.db import models
from accounts.models import Signup
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.validators import MaxValueValidator, MinValueValidator 


class Post(models.Model):
    user = ForeignKey(Signup, on_delete=CASCADE, verbose_name='user', db_index=True)
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()
    nation = models.CharField(max_length=100)
    spot = models.CharField(max_length=100)
    ourMaleNumber = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    ourFemaleNumber = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    yourMaleNumber = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    yourFemaleNumber = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    startDate = models.CharField(max_length=30)
    startTime = models.CharField(max_length=20)
    endDate = models.CharField(max_length=30)
    endTime = models.CharField(max_length=20)
    
    lat = models.FloatField(null=True, blank = True)
    lng = models.FloatField(null=True, blank = True)
    address = models.CharField(max_length=100)
    Confirm = models.BooleanField(default = False)

    def __str__(self):
        return self.title


class Continent(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class applicants(models.Model):
    event = models.ForeignKey(Post,on_delete = models.CASCADE)
    apply = models.ForeignKey(Signup,on_delete = models.CASCADE)

class participants(models.Model):
    event = models.ForeignKey(Post,on_delete=models.CASCADE)
    participate= models.ForeignKey(Signup,on_delete = models.CASCADE)

class Rating(models.Model):
    event = models.ForeignKey(Post,related_name='event',on_delete = models.CASCADE)
    reviewer = models.ForeignKey(Signup,related_name='reviewer',on_delete=models.CASCADE) 
    reviewee = models.ForeignKey(Signup,related_name='reviewee',on_delete=models.CASCADE)
    star = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    contents = models.TextField(blank=True)

    def __str__(self):
        return self.reviewer.nickname +"->"+self.reviewee.nickname

class Country(models.Model):
    country = models.ForeignKey(Continent, on_delete=models.CASCADE)
    cont = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name