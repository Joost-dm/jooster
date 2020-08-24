from io import BytesIO
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import send_mail
from django.db import models
from resizeimage import resizeimage
from rest_framework.authtoken.models import Token
from main.settings import USER_SETTINGS
from django.db.models import ObjectDoesNotExist


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
        """ User's profile update handler. """
        try:
            self.avatar_update_handler()
        except ObjectDoesNotExist:
            send_mail('Новый пользователь!', 'Зарегистрирован новый пользователь: ' + self.displayed,
                      'joost.mail@gmail.com', ['vasiliishirokov@gmail.com'], fail_silently=True)
        super(CustomUser, self).save(*args, **kwargs)

    def avatar_update_handler(self):
        """ Downloaded avatar image update handler. """

        user = CustomUser.objects.get(id=self.id)
        if user.avatar != self.avatar:
            self.get_avatar_ext()
            self.generate_avatar_name()
            self.resize_avatar()
            # self.delete_current_avatar()

    def get_avatar_ext(self):
        """ Parses an avatar image extension. """

        user_avatar_ext = self.avatar.name.split('.')[-1]
        if user_avatar_ext.upper() == 'JPG':
            user_avatar_ext = 'jpeg'
        self.user_avatar_ext = user_avatar_ext

    def resize_avatar(self):
        """ Compresses user's avatar image. New sizes declared at project settings. """

        user_avatar = Image.open(self.avatar)
        avatar_settings = USER_SETTINGS['USER_AVATAR_SETTINGS']
        new_user_avatar = resizeimage.resize_cover(
            user_avatar,
            [avatar_settings['COMPRESSED_WIDTH'], avatar_settings['COMPRESSED_HEIGHT']]
        )
        new_user_avatar_io = BytesIO()
        new_user_avatar.save(new_user_avatar_io, format=self.user_avatar_ext)

        self.avatar = InMemoryUploadedFile(new_user_avatar_io, None, self.avatar.name, 'image/' + self.user_avatar_ext,
                                           new_user_avatar_io.tell(), None)

    # For using with local storage
    """
    def delete_current_avatar(self):
      
        try:
            user = CustomUser.objects.get(id=self.id)
        except IntegrityError:
            raise ValidationError('Некорректный пользователь.')

        storage, path = user.avatar.storage, user.avatar.path

        if self.avatar.name in path:
            storage.delete(path)"""

    def generate_avatar_name(self):
        """ Generates an user's avatar image name according project settings."""

        avatar_settings = USER_SETTINGS['USER_AVATAR_SETTINGS']
        self.avatar.name = avatar_settings['AVATAR_IMAGE_NAME'] + '.' + self.user_avatar_ext

    AVATAR_FIELD = 'avatar'
    REQUIRED_FIELDS = ['email', 'avatar', 'displayed', 'foreign_avatar_url']
