from rest_framework import serializers
from .models import User, Conversation, Message

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(source='message_id.conversation_id', read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'message_body', 'sent_at', 'created_at']

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


# --- Conversation Serializer with Nested Messages ---
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']
