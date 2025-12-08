from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user."""
    def unread_for_user(self, user):
        return (
            self.filter(receiver=user, read=False)
                .only('id', 'sender_id', 'receiver_id', 'content', 'timestamp')
        )

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    objects = models.Manager()
    unread = UnreadMessagesManager()
    parent_message = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    edited = models.BooleanField(default=False)  # Tracks if message was edited
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"
    
    def get_thread(self):
        """
        Recursively build a nested list/dict of all replies.
        Returns a structured thread tree.
        """
        thread = {
            "id": self.id,
            "sender": self.sender.username,
            "content": self.content,
            "timestamp": self.timestamp,
            "replies": []
        }

        # Prefetch replies efficiently
        replies = self.replies.all().select_related("sender").prefetch_related("replies")

        for reply in replies:
            thread["replies"].append(reply.get_thread())

        return thread


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID: {self.message.id}"
    

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message ID {self.message.id} at {self.edited_at}"
    


