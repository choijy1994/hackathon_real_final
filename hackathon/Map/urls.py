from django.contrib import admin
from django.urls import path
from Map import views
from django.conf.urls import url
urlpatterns = [
    path('map/', views.map, name="map"),
    url(r'address/$', views.address_data, name = 'address'),

    url(r'latlng/$', views.latlng_data, name = 'latlng'),
]