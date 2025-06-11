# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log the user out before deleting
    user.delete()    # This will trigger post_delete signal
    return redirect('home')  # Redirect to homepage or goodbye page

def conversation_view(request):
    # Get only top-level messages (those that are not replies)
    messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )

    context = {
        'messages': messages,  # replies will be available via message.replies.all
    }
    return render(request, 'messaging/conversation.html', context)
