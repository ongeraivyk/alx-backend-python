from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Message

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)           # Log the user out first
        user.delete()             # This triggers the post_delete signal
        return HttpResponse("Your account has been deleted successfully.")

    return HttpResponse("Send a POST request to delete your account.")


def inbox_unread(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user)

    return render(request, 'inbox_unread.html', {
        'unread_messages': unread_messages
    })
