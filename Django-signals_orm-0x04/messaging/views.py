# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message, Conversation
from django.db.models import Prefetch
from .forms import MessageForm

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log the user out before deleting
    user.delete()    
    return redirect('home')  # Redirect to homepage or goodbye page

def build_threaded_messages(messages):
    # Dictionary to hold children replies
    reply_dict = {message.id: [] for message in messages}
    message_dict = {message.id: message for message in messages}

    # Group replies under parent
    for message in messages:
        if message.parent_message_id:
            reply_dict[message.parent_message_id].append(message)

    # Recursive function to get messages with nested replies
    def attach_replies(message):
        message.replies_list = reply_dict[message.id]
        for reply in message.replies_list:
            attach_replies(reply)

    # Build threaded list
    top_level = [msg for msg in messages if msg.parent_message is None]
    for msg in top_level:
        attach_replies(msg)

    return top_level


def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        sender = request.user
        if form.is_valid():
            receiver = conversation.participants.exclude(id=sender.id).first()
            new_msg = form.save(commit=False)
            new_msg.sender = sender
            new_msg.receiver = receiver
            new_msg.conversation = conversation
            new_msg.save()
            return redirect('conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()

    all_messages = Message.objects.filter(conversation=conversation).select_related(
        'sender', 'receiver', 'parent_message'
    ).order_by('timestamp')

    threaded_messages = build_threaded_messages(all_messages)

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': threaded_messages,
        'form': form
    })
    
def inbox(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user).only(
        'id', 'sender', 'content', 'timestamp'
    )
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})
