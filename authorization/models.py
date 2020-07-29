from io import BytesIO
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from resizeimage import resizeimage
from rest_framework.authtoken.models import Token


def generate_avatar_path(obj, filename):
    """ Generates an unique path to user's avatar dir according to user's id. """

    return 'images/avatars/' + str(obj.id) + '/' + filename


class CustomUser(AbstractUser):
    """Extends base django user model"""

    displayed = models.CharField(
        max_length=40,
        unique=True,
        verbose_name='отоброжаемое имя'
    )

    avatar = models.ImageField(
        default='images/avatars/default_avatar.png',
        upload_to=generate_avatar_path,
        verbose_name='аватар',
    )

    foreign_avatar_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='аватар из стороних источников'
    )

    def save(self, *args, **kwargs):
        """ Compresses an avatar image to fix size. """

        image = Image.open(self.avatar)
        image_ext = self.avatar.name.split('.')[-1]
        new_image = resizeimage.resize_cover(image, [100, 100])

        new_image_io = BytesIO()
        new_image.save(new_image_io, format=image_ext)

        self.avatar = InMemoryUploadedFile(new_image_io, None, self.avatar.name, 'image/' + image_ext,
                                          new_image_io.tell(), None)

        super(CustomUser, self).save(*args, **kwargs)

    AVATAR_FIELD = 'avatar'
    REQUIRED_FIELDS = ['email', 'avatar', 'displayed', 'foreign_avatar_url']
