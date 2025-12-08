from django.contrib import admin
from .models import User, Conversation, Message
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    pass

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('id', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'sent_at')
=======
    list_display = ('conversation_id', 'created_at')  # corrected

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation', 'sender', 'sent_at')  # corrected
>>>>>>> 05275e1 (Implement JWT authentication, permissions, and messaging models)
