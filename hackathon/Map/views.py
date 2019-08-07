import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from Board.models import Post
import datetime



# Create your views here.


def latlng_data(request):
    queryset = list(Post.objects.values('lat', 'lng'))
    one = Post.objects.all()
    i = 0
    for g in one:
        try:
            day = g.endDate +'  '+ g.endTime
            result = datetime.datetime.strptime(day,"%b %d, %Y %H:%M %p")
            now = datetime.datetime.now()
            # for i in queryset:
            if now>result:
                queryset[i]['date'] = False 
            else:
                queryset[i]['date'] = True  
            i += 1    
        except:
            day = g.endDate
            result = datetime.datetime.strptime(day,"%b %d, %Y")
            now = datetime.datetime.now()
            # for i in queryset:
            if now>result:
                queryset[i]['date'] = False 
            else:
                queryset[i]['date'] = True  
            i += 1 
    return JsonResponse(dict(post = list(queryset)))


def address_data(request):
    queryset = list(Post.objects.values('address'))
    one = Post.objects.all()
    i = 0
    for g in one:
        try:
            day = g.endDate +'  '+ g.endTime
            result = datetime.datetime.strptime(day,"%b %d, %Y %H:%M %p")
            now = datetime.datetime.now()
            # for i in queryset:
            if now>result:
                queryset[i]['date'] = False 
            else:
                queryset[i]['date'] = True  
            i += 1    
        except:
            day = g.endDate
            result = datetime.datetime.strptime(day,"%b %d, %Y")
            now = datetime.datetime.now()
            # for i in queryset:
            if now>result:
                queryset[i]['date'] = False
            else:
                queryset[i]['date'] = True  
            i += 1
    return JsonResponse(dict(address=list(queryset)))


def map(request):
    return render(request, 'map.html')