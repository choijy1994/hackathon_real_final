from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model,login, authenticate
from django.contrib import auth
from django import forms
from django.views import generic
from .forms import UserCreationMultiForm,LoginForm,UpdateForm,UserCreationForm
from .models import Signup,Relationship
from Board.models import Post,participants,Rating
from chatting.models import MessageModel
from django.urls import reverse_lazy
from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import datetime

def home(request):
    return render(request, 'main.html')

def main(request):
    return render(request, 'home.html')

def signup(request):
    if request.method=="POST":
        form = UserCreationMultiForm(request.POST,request.FILES)
        if form.is_valid():
            User = form['User'].save()
            new_user = form['signup'].save(commit=False)
            print(new_user.image)
            new_user.user = User
            new_user.save()
            return redirect('login')
    else:
        form=UserCreationMultiForm()
    return render(request,'registration/signup.html',{'form':form})

@login_required
def mypage(request):
    conn_user=request.user
    conn_profile=Signup.objects.get(user=conn_user)

    if not conn_profile.image:
        image=""
    else:
        image=conn_profile.image.url

    context={
        'userid':conn_user.username,
        'name': conn_profile.name, 
        'nickname':conn_profile.nickname,
        'gender':conn_profile.gender,
        'birth': conn_profile.birth,
        'image': image,
        'intro': conn_profile.intro,
    }
    return render(request, 'registration/mypage.html', context=context)


# 회원 프로필 update - 조정수 담당
def update(request,name):
    User=request.user
    prof=Signup.objects.get(user=User)
    if request.method=='POST':
        form = UpdateForm(request.POST,request.FILES)
        if form.is_valid():
            User = request.user
            profile= Signup.objects.filter(user=User)
            prof = Signup.objects.get(user=User)
            # f = File(request.FILES)
            if request.FILES:
                prof.image = request.FILES['image']
            if request.POST:
                prof.nickname = request.POST['nickname']
                prof.intro = request.POST['intro']
                prof.save()
                return redirect('mypage')
    else:
        form=UpdateForm(instance=prof)
    return render(request,'registration/update.html',{'form':form})

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('loginhome')
        else:   
            return render(request, 'registration/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'registration/login.html')

def loginhome(request):
    Usr = Signup.objects.get(user = request.user)
    unread = MessageModel.objects.filter(recipient = Usr,is_read = False)

    Unread= unread.count()
    
    group= participants.objects.filter(participate = Usr)
    dic1 = {}
    dic2 = {}
    dic3 = {}
    flag = False
    for g in group:
        if not g.event.Confirm:
            continue
        party = participants.objects.filter(event=g.event)
        l = []
        l2 = []
        l3 = []
        
        if g.event.endTime == '':
            day = g.event.endDate
            result = datetime.datetime.strptime(day,"%b %d, %Y")
        else:
            day = g.event.endDate + '  '+g.event.endTime
            result = datetime.datetime.strptime(day,"%b %d, %Y %H:%M %p")
        now = datetime.datetime.now()
        for p in party:
            if p.participate == Usr:
                continue
            if now>result:
                if Rating.objects.filter(event=g.event,reviewer = Usr,reviewee=p.participate).count()==0:
                    l.append(p)
                else:
                    l2.append(p)
            else:
                l3.append(p)
        if now>result:
            dic1[g.event] = l
            dic2[g.event] = l2
        else:
            dic3[g.event] = l3
        
        
        if len(l)>0:
            flag = True
        

    if flag:
        context = {
            'dic1':dic1,
            'dic2':dic2,
            'dic3':dic3,
            'flag':flag,
            'group':group,
            'party':party,
            'Unread':Unread,
        }
        return render(request, 'mygroup.html',context)
    else:
        context = {
            'Unread':Unread,
        }
        return render(request,'registration/loginhome.html',context)

# def logout(request):
#    logout(request)
#    return HttpResponseRedirect('home')

def delete(request):
    if request.method == 'POST':
        target_pass = request.user.password
        cur_pas = request.POST.get('currentPassword')
        check_result = check_password(cur_pas,target_pass)
        if check_result:
            request.user.delete()
            return redirect('registration/deletesuccess')   
        else: 
            return render(request, 'delete.html', {'error': '비밀번호가 틀렸습니다.'})    
    return render(request, 'registration/delete.html')

def deletesuccess(request):
    return render(request, 'registration/deletesuccess.html')

def show_friends(request):
    return render(request,'chatting/friends.html')

def add_friend(request,post_id):
    post = get_object_or_404(Post,pk = post_id)
    
    from_signup = Signup.objects.get(user = request.user)

    Relationship.objects.get_or_create(
        from_person = from_signup,
        to_person  = post.user,
    )
    Relationship.objects.get_or_create(
        from_person = post.user,
        to_person  = from_signup,
    )
    context = {
        'from_user':post.user.nickname,
        'to_user':from_signup.nickname,
    }

    return render(request, 'chatting/friends.html', context)
    