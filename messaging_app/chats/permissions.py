from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    - Allow only authenticated users.
    - Allow only participants of a conversation to access related messages.
    """

    def has_permission(self, request, view):
        # Allow access only to authenticated users globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        if isinstance(obj, Message):
            return request.user in obj.message_id.participants.all()
            if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                return is_participant

        return False
