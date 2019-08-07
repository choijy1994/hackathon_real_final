from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                              CASCADE)
from django.db import models
from accounts.models import Signup
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.validators import MaxValueValidator, MinValueValidator 

class MessageModel(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    user = ForeignKey(Signup, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(Signup, on_delete=CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField('body')

    is_read = models.BooleanField(default = False)

    
    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.nickname))
        print("user.idd {}".format(self.recipient.nickname))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.nickname), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.nickname), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'chatting'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)


