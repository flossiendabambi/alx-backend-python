from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import User, Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
        print(f"🔔 Notification created for {instance.receiver.username}")


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            # Create MessageHistory before saving new content
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=instance.edited_by  # manually set before save
            )
            instance.edited = True
            
@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete messages where user was sender or receiver
    Message.objects.filter(Q(sender=instance) | Q(receiver=instance)).delete()

    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories where user edited messages
    MessageHistory.objects.filter(edited_by=instance).delete()
