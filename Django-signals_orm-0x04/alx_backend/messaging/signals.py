from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # Message is new, no history needed
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content has changed, log the old content
    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True  # Mark message as edited


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Delete messages sent by user
    sent_messages = Message.objects.filter(sender=instance)
    sent_messages.delete()

    # Delete messages received by user
    received_messages = Message.objects.filter(receiver=instance)
    received_messages.delete()

    # Delete all notifications belonging to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message history linked to messages the user participated in
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()