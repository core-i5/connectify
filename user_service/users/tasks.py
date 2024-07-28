from celery import shared_task
import requests

@shared_task
def notify_post_service(user_id, action):
    url = f'http://post_service:8000/api/users/{user_id}/'
    if action == 'created':
        response = requests.post(url, data={})
    elif action == 'updated':
        response = requests.put(url, data={})
    elif action == 'deleted':
        response = requests.delete(url)
    return response.status_code