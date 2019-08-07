from django.contrib import admin
from .models import Continent, Country, Post,participants,applicants,Rating

# Register your models here.

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Post)
admin.site.register(participants)
admin.site.register(applicants)
admin.site.register(Rating)
