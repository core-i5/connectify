from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    mobile_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
