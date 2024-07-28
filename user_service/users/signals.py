from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .tasks import notify_post_service

User = get_user_model()

@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    if created:
        notify_post_service.delay(instance.id, 'created')
    else:
        notify_post_service.delay(instance.id, 'updated')

@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    notify_post_service.delay(instance.id, 'deleted')