from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Comment
from .models import Notification

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.user:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            post=instance.post,
            comment=instance,
            message=f"{instance.user.username} commented: {instance.content[:30]}..."
        )