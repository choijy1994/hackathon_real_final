from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                              CASCADE)
from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.validators import MaxValueValidator, MinValueValidator 


class Signup(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,verbose_name='user',related_name='user')
    name = models.CharField(max_length=100)
    nickname = models.CharField(blank=True,max_length=15)
    birth = models.DateField()
    GENDER = (
        ('F','female'),
        ('M','male'),
    )
    gender = models.CharField(max_length=1,choices = GENDER)
    phone = models.IntegerField()
    image = models.ImageField(blank = True,upload_to='path/',null=True)
    intro = models.TextField(blank=True,help_text = 'Introduce yourself')
    relationships = models.ManyToManyField('self',through='Relationship',symmetrical = False,related_name='related_to',verbose_name='relation')
    

    def __str__(self):
        return self.user.username




class Relationship(models.Model):
    from_person = models.ForeignKey(Signup,related_name='from_person',on_delete=models.CASCADE)
    to_person = models.ForeignKey(Signup,related_name='to_person',on_delete = models.CASCADE)

