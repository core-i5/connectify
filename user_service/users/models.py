from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    mobile_no = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following")