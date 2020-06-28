from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token

class CustomUser(AbstractUser):
    avatar = models.ImageField(blank=True, default='images/avatars/default_avatar.png', upload_to='images/avatars/')
    AVATAR_FIELD = 'avatar'
    REQUIRED_FIELDS = ['email']



