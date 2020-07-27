from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    """Extends base django user model"""

    displayed = models.CharField(
        max_length=40,
        unique=True,
        verbose_name='Отоброжаемое имя'
    )

    avatar = models.ImageField(
        default='images/avatars/default_avatar.png',
        upload_to='images/avatars/',
        verbose_name='аватар'
    )

    foreign_avatar_url = models.URLField(
        null=True
    )

    AVATAR_FIELD = 'avatar'
    REQUIRED_FIELDS = ['email', 'avatar', 'displayed', 'foreign_avatar_url']



