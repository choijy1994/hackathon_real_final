from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from chat import settings
from chatting.serializers import MessageModelSerializer, UserModelSerializer,SignupModelSerializer,RelationshipsSerializer,PostSerializer
from chatting.models import MessageModel,Signup
from Board.models import Post


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination
    
    

    def list(self, request, *args, **kwargs):
        User_signup = Signup.objects.get(user=request.user)
        self.queryset = self.queryset.filter(Q(recipient=User_signup) |
                                             Q(user=User_signup))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=User_signup, user__nickname=target) |
                Q(recipient__nickname=target, user=User_signup))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        User_signup = Signup.objects.get(user=request.user)
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=User_signup) |
                                 Q(user=User_signup),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)

class SignupModelViewSet(ModelViewSet):
    queryset = Signup.objects.all()
    serializer_class = SignupModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        #self.queryset = self.queryset.filter(user=request.user)
        return super(SignupModelViewSet, self).list(request, *args, **kwargs)

class RelationModelViewSet(ModelViewSet):
    queryset = Signup.objects.all()
    serializer_class = RelationshipsSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.filter(user=request.user)
        return super(RelationModelViewSet, self).list(request, *args, **kwargs)

    
class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    allowed_methods = ('GET','HEAD','OPTIONS')
    pagination_class= None

