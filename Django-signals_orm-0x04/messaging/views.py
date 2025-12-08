from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from .models import Message

def get_all_replies(message):
    replies = message.replies.all().select_related("sender", "receiver")
    all_replies = []
    for reply in replies:
        all_replies.append(reply)
        all_replies.extend(get_all_replies(reply))
    return all_replies


@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)           # Log the user out first
        user.delete()             # This triggers the post_delete signal
        return HttpResponse("Your account has been deleted successfully.")

    return HttpResponse("Send a POST request to delete your account.")

@login_required
def unread_inbox(request):
    # Fetch unread messages and select only necessary fields
    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .only("id", "sender_id", "receiver_id", "content", "timestamp")
    )
    
    return render(request, "messages/unread_inbox.html", {
        "unread_messages": unread_messages
    })


@login_required
@cache_page(60)
def conversation_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    messages = (
        Message.objects.filter(
            sender=request.user, receiver=other_user
        )
        | Message.objects.filter(
            sender=other_user, receiver=request.user
        )
    ).select_related("sender", "receiver", "parent_message").prefetch_related("replies")

    # Build threaded structure
    threaded_messages = []
    for msg in messages:
        if msg.parent_message is None:  # top-level messages only
            threaded_messages.append({
                "message": msg,
                "replies": get_all_replies(msg)
            })

    return render(request, "messages/conversation.html", {
        "messages": threaded_messages,
        "other_user": other_user
    })