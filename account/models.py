from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_financialstaff = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to = 'avatars/',default = 'avatar.png')
    phone_number = models.CharField(max_length=11,blank=True)
    