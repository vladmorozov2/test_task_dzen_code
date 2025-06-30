from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .consumers import notify_new_comment


@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    print("comment_created signal triggered")
    if created:
        notify_new_comment(instance)
