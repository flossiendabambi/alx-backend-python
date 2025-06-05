from rest_framework import permissions
from .models import Conversation, Message

class IsConversationParticipant(permissions.BasePermission):
    """
    Allows access only to users who are participants in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        return False

class IsMessageParticipant(permissions.BasePermission):
    """
    Allows access only to messages where the user is a participant in the related conversation.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            return request.user in obj.message_id.participants.all()
        return False
