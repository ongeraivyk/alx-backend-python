from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class NotificationSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='pass')
        self.receiver = User.objects.create_user(username='bob', password='pass')

    def test_notification_created(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello Bob!')
        notification = Notification.objects.filter(user=self.receiver, message=msg).first()
        self.assertIsNotNone(notification)
        self.assertFalse(notification.read)


class MessageEditTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='pass')
        self.receiver = User.objects.create_user(username='bob', password='pass')
        self.message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello Bob!')

    def test_message_edit_creates_history(self):
        # Edit the message
        self.message.content = 'Hello Bob! Updated'
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, 'Hello Bob!')
        self.assertTrue(Message.objects.get(pk=self.message.pk).edited)