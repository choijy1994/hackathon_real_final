from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from chatting.api import MessageModelViewSet, UserModelViewSet,SignupModelViewSet,RelationModelViewSet,PostModelViewSet
from .views import Message_read

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, base_name='message-api')
router.register(r'user', UserModelViewSet, base_name='user-api')
router.register(r'Signup',SignupModelViewSet,base_name = 'signup-api')
router.register(r'relationship',RelationModelViewSet,base_name = 'relationship-api')
router.register(r'Post',PostModelViewSet,base_name='Post-api')

urlpatterns = [
    path(r'chat/api/v1/', include(router.urls)),
    path('chat/', login_required(
        TemplateView.as_view(template_name='chatting/chat.html')), name='chat'),
    path('show_friends/',login_required(
        TemplateView.as_view(template_name='chatting/friends.html')),name='show_friends'),
    
    path(r'message_read',Message_read,name='message_read'),

]

