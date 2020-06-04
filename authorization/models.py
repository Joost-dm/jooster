from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token

class CustomUser(AbstractUser):
    avatar = models.ImageField(blank=True, null=True, upload_to='images/')
    AVATAR_FIELD = 'avatar'
    REQUIRED_FIELDS = ['email', 'avatar']



