from django.urls import path
from .views import conversation_messages

urlpatterns = [
    path('conversation/<int:conversation_id>/', conversation_messages, name='conversation_messages'),
]
