from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']

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
        if request_user.id not in participant_ids:
            participant_ids.append(request_user.id)

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(id__in=participant_ids))
        return conversation

class MessageSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sent_at']

    def create(self, validated_data):
        conversation_id = validated_data.pop('conversation_id')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation not found.")

        return Message.objects.create(
            conversation=conversation,
            sender=self.context['request'].user,
            **validated_data
        )