from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number']

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )
    participants_info = UserSerializer(source='participants', many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participants_info']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participants', [])
        request_user = self.context['request'].user

        # Ensure creator is included
        if request_user.user_id not in participant_ids:
            participant_ids.append(request_user.user_id)

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(user_id__in=participant_ids))
        return conversation

class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(write_only=True)
    message_id = ConversationSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'message_id', 'message_body', 'sent_at', 'created_at']

    def create(self, validated_data):
        conversation_id = validated_data.pop('conversation_id')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation not found.")

        return Message.objects.create(message_id=conversation, **validated_data)
