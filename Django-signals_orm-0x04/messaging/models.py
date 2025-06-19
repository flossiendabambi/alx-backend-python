from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    

    def __str__(self):
        return f"Conversation {self.id}"
    
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Filter unread messages for the given user (receiver)
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')
    
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE  # delete replies if parent is deleted
    ) # parent_message

    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()
    
    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:30]}"
    
        class Meta:
            ordering = ['timestamp']

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # the receiver of the message
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about Message ID {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
       return f"Edit of Message {self.message.id} by {self.edited_by} on {self.edited_at}"
