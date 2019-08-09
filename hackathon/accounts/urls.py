from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import signup,mypage,update,login,loginhome,add_friend,delete,deletesuccess
from Board import views
from chat import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('mypage/',mypage,name='mypage'),
    path('mypage/update/<str:name>',update,name='update'),
    path('login/',login, name='login'),

    path('mypage/myfriend<int:post_id>', views.myfriend, name='myfriend'),

    path('loginhome',loginhome,name='loginhome'),
    
    path('add_friends/<int:post_id>',add_friend,name="add_friend"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('loginhome/delete/',delete, name="delete"),
    path('deletesuccess/', deletesuccess, name="deletesuccess"),
    path('loginhome/delete/registration/deletesuccess', deletesuccess, name="deletesuccess")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)