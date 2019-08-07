from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from chatting.models import MessageModel,Signup
from Board.models import Post
from rest_framework.serializers import ModelSerializer, CharField

class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.nickname', read_only=True)
    recipient = CharField(source='recipient.nickname')

    def create(self, validated_data):
        user = self.context['request'].user
        Signup_user = Signup.objects.get(user=user)
        recipient = get_object_or_404(
            Signup, nickname=validated_data['recipient']['nickname'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=Signup_user,is_read = False) 
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body','is_read')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class SignupModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)

    class Meta:
        model = Signup
        fields = ('user','nickname',)

class RelationshipsSerializer(ModelSerializer):
    relationships = SignupModelSerializer(many = True,read_only=True)

    class Meta:
        model = Signup
        fields = ('relationships',)


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('title','user',)
