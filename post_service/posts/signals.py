from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Discussion, Comment
from .tasks import update_view_count

@receiver(post_save, sender=Discussion)
def discussion_saved(sender, instance, created, **kwargs):
    if created:
        update_view_count.delay(instance.id)
