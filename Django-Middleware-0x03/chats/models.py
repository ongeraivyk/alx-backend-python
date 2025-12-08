# messaging_app/chats/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ('guest', 'Guest'),
    ('host', 'Host'),
    ('admin', 'Admin'),
)


class User(AbstractUser):
    """
    Custom user extending AbstractUser.
<<<<<<< HEAD
    Includes built-in fields: password, first_name, last_name.
    Primary key is UUID and email is unique.
    """

    Custom user extending AbstractUser.
=======
>>>>>>> 05275e1 (Implement JWT authentication, permissions, and messaging models)
    Primary key is UUID and email is unique.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.email})"


class Conversation(models.Model):
    """
    Conversation between multiple users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Message sent within a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} by {self.sender}"
