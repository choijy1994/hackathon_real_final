from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model,login, authenticate
from django.contrib import auth
from django import forms
from django.views import generic
from .forms import NewPost
from accounts.models import Signup,Relationship
from .models import Post
from django.urls import reverse_lazy
from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from Board.models import Continent, Country,applicants,participants
from Board.models import Rating
from django.db.models import Avg
import datetime


def post_read(request):
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    nick = Signup.objects.values('user', 'nickname')

    context = {
        'posts':posts,
        'nick':nick,
    }
    return render(request, 'boardmain.html', context)

def post_search(request):
    word = request.GET.get('q')

    searched_post = Post.objects.filter(Q(title__icontains=word) | Q(spot__icontains=word)).distinct()
    nick = Signup.objects.values('user', 'nickname')

    #posts = Post.objects.order_by('-pub_date')
    #일단 순서는 나중에

    paginator = Paginator(searched_post, 5)
    page = request.GET.get('page')
    searched_post = paginator.get_page(page)

    context = {
        'posts':searched_post,
        'nick':nick,
    }

    return render(request, 'search.html', context)

def post_create(request):
    # 새로운 데이터, 즉 새로운 블로그 글을 저장하는 역할 == POST
    # 글쓰기 버튼을 눌렀을 시 글쓰기 페이지를 띄워주는 역할 == GET (즉, POS가 아니었을 때)
    # 이 둘은 request의 형식에 따라 구분한다.

    if request.method == 'POST':
        # 우선 어떤 형식의 입력 공간으로부터 입력을 받았는지 알려주기
        form = NewPost(request.POST)
        if form.is_valid:
            # 실질적으로 저장하는 과정
            post = form.save(commit=False) #입력받은 내용을 save할 것입니까 묻는건데 아직 안 하는 것이다. pub_date가 안들어왔기 때문.
            post.pub_date = timezone.now() # pub_date를 post에 자동으로 담아주세요
            Usr = Signup.objects.get(user=request.user)
            post.user = Usr
            post.startDate = request.POST['startDate']
            post.startTime = request.POST['startTime']
            post.endDate = request.POST['endDate']
            post.endTime = request.POST['endTime']
            
            post.save() # 이젠 post 저장해주세요
            participants.objects.create(event=post,participate=post.user)

            return redirect('boardmain') # post 저장이 완료되면 main으로 redirection 시켜주세요

    else:
        form = NewPost()
        return render(request, 'newpost.html', {'form':form})

def post_update(request, pk):
    # 수정하고자 하는 특정 블로그 글을 가져온다
    post = get_object_or_404(Post, pk= pk)

    if request.method == "POST":
        # 해당하는 블로그 객체 번호(pk)에 맞는 입력 공간
        # instance 는 객체라고 생각해도 무방
        form = NewPost(request.POST, instance = post)
    
        if form.is_valid():
            post = form.save(commit = False)
            # 저장하기전 상태의 데이터값을 자동으로 form에 채워줌
            post.startDate = request.POST['startDate']
            post.startTime = request.POST['startTime']
            post.endDate = request.POST['endDate']
            post.endTime = request.POST['endTime']
            post.save()
            return redirect('contents_read', pk = pk) # post 저장이 완료되면 boardmain으로 redirection 시켜주세요
    else:
        form = NewPost(instance=post)
    
    return render(request, 'boardEdit.html', {'form': form})

def post_delete(request, pk):
    # 삭제하고자 하는 특정 블로그 글을 가져온다
    post = get_object_or_404(Post, pk = pk)

    # Post 객체를 가져올 것이고. delete 함수의 인자로 받은 pk를 설정
    post.delete()

    return redirect('boardmain')

def contents_read(request, pk):
    # 제목을 눌렀을 때 해당 게시글의 내용을 받아온다
    post = get_object_or_404(Post, pk= pk)
    nick = Signup.objects.values('user', 'nickname')
    check = post.user.user
    #print(check)

    return render(request, 'boardcontents.html', {'post':post, 'nick':nick, 'check':check})


def select(request):
    continents = Continent.objects.all

    asia = Country.objects.filter(cont__icontains="아시아")
    #print(asia)
    eu = Country.objects.filter(cont__icontains="유럽")

    context = {
        'continents' : continents,
        'asia' : asia,
        'eu' : eu,
    }
    return render(request, 'select.html', context)


# 종윤이가 해결할 곳
def myfriend(request, pk):
    post = get_object_or_404(Post,pk=pk)   
    applicant = applicants.objects.filter(event=post)
    participant = participants.objects.filter(event=post)
    context = {
        'post':post,
        'applicant':applicant,
        'participant' :participant,
    } 
    return render(request, 'registration/myfriend.html', context)

def apply(request,pk):
    post = get_object_or_404(Post, pk= pk)
    post_usr = post.user
    apply_user = Signup.objects.get(user = request.user)
    applicants.objects.get_or_create(event=post,apply=apply_user)
    
    context = {
        'post':post,
  
    }
    return redirect('contents_read',pk=pk)


def approve(request,user_id,post_id):
    post = Post.objects.get(pk=post_id)
    Usr = Signup.objects.get(pk=user_id)
    participants.objects.get_or_create(event=post,participate = Usr)
    applicants.objects.get(event=post,apply=Usr).delete()
    applicant = applicants.objects.filter(event = post)
    participant = participants.objects.filter(event = post)
    context = {
        'post':post,
        'applicant':applicant,
        'participant':participant,
    }
    return render(request, 'registration/myfriend.html', context)


def deny(request,user_id,post_id):
    post = get_object_or_404(Post,pk=post_id)
    Usr = Signup.objects.get(pk = user_id)
    applicants.objects.get(event=post,apply=Usr).delete()
    applicant = applicants.objects.filter(event = post)
    participant = participants.objects.filter(event = post)
    context = {
        'post':post,
        'applicant':applicant,
        'participant':participant,
    }
    return render(request, 'registration/myfriend.html', context)


def cancel(request,user_id,post_id):
    post = get_object_or_404(Post,pk=post_id)
    Usr = Signup.objects.get(pk=user_id)
    participants.objects.get(event=post,participate=Usr).delete()
    applicants.objects.get_or_create(event=post,apply=Usr)
    applicant = applicants.objects.filter(event = post)
    participant = participants.objects.filter(event = post)
    context = {
        'post':post,
        'applicant':applicant,
        'participant':participant,
    }
    return render(request, 'registration/myfriend.html', context)


def detail(request, user_id):
    try:
        
        profile = Signup.objects.get(pk=user_id)
    except:
        raise Http404

    # editable=False
    
    context={
        'userid': profile.user,
        'name': profile.name, 
        'nickname':profile.nickname,
        'gender':profile.gender,
        'birth': profile.birth,
        'image': profile.image,
        'intro': profile.intro,
    }

    if request.user.is_authenticated and request.user==profile.user:
        return render(request, 'registration/mypage.html', context=context)
    else:
        return render(request, 'registration/detail.html', context)

def ratingview(request, user_id):
    # reviews=Rating.objects.all()
    # averages=reviews.aggregate(총평점=Avg('star'))
    
    target_sign = Signup.objects.get(pk = user_id)
    rate = Rating.objects.filter(reviewee=target_sign)
    if rate.count()>0:
        average1=rate.aggregate(총평점=Avg('star'))
        average = round(average1['총평점'],2)
    else:
       average = 0
    
    context={
        'rate':rate,
        'average':average,
        }

    return render(request, 'registration/ratingview.html', context)

def mypost(request):
    user = request.user
    name = Signup.objects.get(user=user)
    #print(name)
    posts = Post.objects.filter(user_id=name)
    #print(posts)
    context = {
        'posts' : posts
    }
    return render(request, 'mypost.html', context)

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
    

def mygroup(request):
    Usr = Signup.objects.get(user = request.user)
    group= participants.objects.filter(participate = Usr)
    dic1 = {}
    dic2 = {}
    dic3 = {}
    for g in group:
        party = participants.objects.filter(event=g.event)
        l = []
        l2=[]
        for p in party:
            if p.participate == Usr:
                continue
            if Rating.objects.filter(event=g.event, reviewer=Usr, reviewee=p.participate).count()>0:
                l2.append(p.participate)
            else:
                l.append(p.participate)
            l.append(p.participate)
        if g.event.startDate != '출발 날짜 설정':
            day = g.event.endDate +'  '+ g.event.endTime
            result = datetime.datetime.strptime(day,"%b %d, %Y %H:%M %p")
            now = datetime.datetime.now()
            if now>result:
                dic1[g.event] = l
            else:
                dic2[g.event] = l
        else:
            dic1[g.event] = l
    flag = False
    context = {
        'flag':flag,
        'dic1':dic1,
        'dic2':dic2,
        'group':group,
        'party':party,
    }
    return render(request,'mygroup.html',context)

def rating(request,user_id,post_id):
    if request.method=='POST':
        user_signup = Signup.objects.get(user =request.user)
        target_sign = Signup.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)
        flag = False
        if Rating.objects.filter(event=post,reviewer=user_signup,reviewee=target_sign).count()>0:
            
            return redirect('mygroup')
        Rating.objects.get_or_create(
            event = post,
            reviewer = user_signup,
            reviewee = target_sign,
            star = request.POST['star'],
            contents = request.POST['contents']
        )
    
    return render(request,'registration/rating.html')


# def dateCheck(StartDate, EndDate, request, in_username):
#     if int(StartDate[-4:]) == int(EndDate[-4:]) or int(StartDate[-4:]) < int(EndDate[-4:]):
#         pass

#     elif int(StartDate[-4:]) > int(EndDate[-4:]):
#         messages.info(request, '날짜 다시 입력해주세요')
#     return HttpResponseRedirect('boardcontents/'+in_username)

# def PrintDate(A):
#     return