import uuid
from django.db import models

# Create your models here.
class User (models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20)
<<<<<<< HEAD
=======
    
    def __str__(self):
        return self.first_name
>>>>>>> 36f6d72 (Serializers)
    
    
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField("User")
    
    def __str__(self):
        return self.conversation_id


class Message(models.Model):
    message_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
=======
    
    def __str__(self):
        return self.message_id
>>>>>>> 36f6d72 (Serializers)
