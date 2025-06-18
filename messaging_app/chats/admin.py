from django.contrib import admin
from .models import User, Conversation, Message

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'id')
    
admin.site.register(Conversation)
admin.site.register(Message)