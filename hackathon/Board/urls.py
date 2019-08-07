from django.urls import path, include
from .views import post_read,post_create, post_update,search_marker, home_create,  post_delete, post_search, contents_read, select, mypost,europe,get_nation, africa, n_america, s_america, aust, asia,apply,myfriend,approve,deny,cancel,detail,ratingview,mygroup,rating,confirm


urlpatterns = [
    path('boardmain/', post_read, name="boardmain"),
    path('newpost/', post_create, name="newpost"),
    path('post_update/<int:pk>', post_update, name="post_update"),
    path('post_delete/<int:pk>', post_delete, name="post_delete"),
    path('post_search/', post_search, name="post_search"),
    path('contents_read/<int:pk>', contents_read, name="contents_read"),
    path('select/', select, name="select"),
    path('mypost/', mypost, name="mypost"),
    path('apply/<int:pk>',apply,name="apply"),
    path('myfriend/<int:pk>',myfriend,name="myfriend"),  
    path('approve/<int:user_id>/<int:post_id>',approve,name='approve'),
    path('deny/<int:user_id>/<int:post_id>',deny,name='deny'),
    path('cancel/<int:user_id>/<int:post_id>',cancel,name='cancel'),
    path('detail/<int:user_id>',detail,name='detail'),
    path('ratingview/<int:user_id>',ratingview,name='ratingview'),
    path('rating/<int:user_id>/<int:post_id>',rating,name='rating'),
    path('confirm/<int:post_id>',confirm,name='confirm'),
    path('mygroup',mygroup,name='mygroup'),
    path('europe/', europe, name="europe"),
    path('asia/', asia, name="asia"),
    path('africa/', africa, name="africa"),
    path('s_america/', s_america, name="s_america"),
    path('n_america/', n_america, name="n_america"),
    path('aust/', aust, name="aust"),
    path('nations/<int:pk>', get_nation, name="get_nation"),
    path('search_marker/', search_marker, name="search_marker"),
    path('home_create/', home_create, name="home_create"),

]