# messaging_app/chats/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for conversations.
    list: list conversations
    create: create conversation and add participants
    retrieve: get conversation with nested messages
    """
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages__sender')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Expected payload:
        {
            "participant_ids": ["uuid1", "uuid2", ...]   # list of user UUIDs
        }
        """
        participant_ids = request.data.get('participant_ids', [])
        if not isinstance(participant_ids, list) or not participant_ids:
            return Response({"detail": "participant_ids (non-empty list) required"},
                            status=status.HTTP_400_BAD_REQUEST)
        # validate users
        users = User.objects.filter(id__in=participant_ids)
        if users.count() != len(participant_ids):
            return Response({"detail": "some participant ids are invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        conv = Conversation.objects.create()
        conv.participants.add(*users)
        serializer = self.get_serializer(conv)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('conversation', 'message_body')


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for messages.
    list: optionally filter by conversation via ?conversation=<uuid>
    create: create a message tied to a conversation (sender set from request.user)
    """
    queryset = Message.objects.all().select_related('sender', 'conversation')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def list(self, request, *args, **kwargs):
        conv_id = request.query_params.get('conversation')
        qs = self.queryset
        if conv_id:
            qs = qs.filter(conversation_id=conv_id)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conv = get_object_or_404(Conversation, id=serializer.validated_data['conversation'].id)
        # If anonymous or not authenticated, you can fill sender differently.
        # For now, require authentication.
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Authentication required to send messages"},
                            status=status.HTTP_403_FORBIDDEN)
        message = Message.objects.create(
            conversation=conv,
            sender=request.user,
            message_body=serializer.validated_data['message_body']
        )
        out_serializer = MessageSerializer(message)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
