from .models import MessageModel
from accounts.models import Signup
import json
from django.http import HttpResponse    
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render

@csrf_exempt
def Message_read(request):
    from django.http import JsonResponse
    if request.method=='POST' and request.is_ajax():
        try:
            id = request.POST['pk']
            Message = MessageModel.objects.get(pk=id)
            user_signup = Signup.objects.get(user = request.user)
            if Message.recipient == user_signup:
                Message.is_read = True
                Message.save()
            return JsonResponse({'status':'Success','msg':'save_successfully'})
        except MessageModel.DoesNotExist:
            return JsonResponse({'status':'Fail','msg':'Object does not exist'})
    else:
        return JsonResponse({'status':'Fail','msg':'Not a valid request'})
    