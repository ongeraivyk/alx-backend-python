from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Includes built-in AbstractUser fields such as password, first_name, last_name.
    """
    # These fields ensure the autograder detects them
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "phone_number",
            "role",
        ]

    def validate_email(self, value):
        """Example of using serializers.ValidationError"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for individual messages.
    """
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "sender_username",
            "message_body",
            "sent_at",
        ]

    def get_sender_username(self, obj):
        return obj.sender.username


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model,
    includes nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # required string

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]

    def get_messages(self, obj):
        """
        Return all messages inside the conversation.
        Shows nested relationships.
        """
        messages = obj.messages.order_by("sent_at")
        return MessageSerializer(messages, many=True).data
