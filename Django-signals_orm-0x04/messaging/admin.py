from django.contrib import admin
from .models import Message, Notification, MessageHistory, Conversation

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)
admin.site.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'participants')