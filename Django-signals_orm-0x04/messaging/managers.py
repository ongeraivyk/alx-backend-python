# messaging/managers.py

from django.db import models
from django.contrib.auth.models import User
from .models import Message

class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user."""
    def unread_for_user(self, user):
        return (
            self.filter(receiver=user, read=False)
                .only("id", "sender_id", "receiver_id", "content", "timestamp")
        )
