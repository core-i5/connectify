from celery import shared_task
from .models import Discussion

@shared_task
def update_view_count(discussion_id):
    try:
        discussion = Discussion.objects.get(id=discussion_id)
        discussion.view_count += 1
        discussion.save()
    except Discussion.DoesNotExist:
        pass
