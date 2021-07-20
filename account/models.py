from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_financialstaff = models.BooleanField(default=True)
    balance = models.IntegerField(default=0 )
    avatar = models.ImageField(upload_to = 'avatars/',default = 'avatar.png')