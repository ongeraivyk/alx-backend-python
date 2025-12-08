from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversations.
    Only shows conversations where the current user is a participant.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Filter conversations to only include those the user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Ensure the creator is added as a participant automatically
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for messages.
    Only shows messages in conversations where the user is a participant.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Only messages in conversations that include the user
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the sender to the logged-in user
        serializer.save(sender=self.request.user)
