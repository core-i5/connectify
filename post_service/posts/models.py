from django.db import models
from django.contrib.auth import get_user_model
from django_elasticsearch_dsl.registries import registry

User = get_user_model()

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='discussions/', null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='discussions')
    created_on = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        registry.update(self)

    def delete(self, *args, **kwargs):
        registry.delete(self)
        super().delete(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments')