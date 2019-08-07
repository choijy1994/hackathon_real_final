from django.contrib import admin
from django.urls import path, include
from accounts.views import home, main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('main/', main, name="main"),
    path('', include('chatting.urls')),
    path('', include('accounts.urls')),
    path('', include('Board.urls')),
    path('', include('Map.urls')),
]
