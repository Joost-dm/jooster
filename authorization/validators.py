import math
from django.core.files.images import get_image_dimensions
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from authorization.models import CustomUser


class UserDownloadedAvatarHandler(object):
    requires_context = True

    def __init__(self, image, context):
        self.max_w = 1200
        self.max_h = 1200
        self.max_size = 200000

        self.image = image
        self.context = context.context

        self.image_handler()

    def __call__(self, image, context):
        self.image = image
        self.context = context
        self.image_handler()

    def image_handler(self):

        self.validate_image()
        self.generate_avatar_name()
        self.delete_current_avatar()

    def get_request_user(self):

        try:
            self.user = CustomUser.objects.get(username=self.context['request'].user)
        except IntegrityError:
            raise ValidationError('Переданы некорректные данные авторизации.')

    def validate_image(self):

        image_size = self.image.size
        image_w, image_h = get_image_dimensions(self.image)

        if image_size > self.max_size:
            raise ValidationError(
                'Превышен максимальный размер изображения. ('
                + str(math.floor(image_size/1000)) + 'кб при допустимых '
                + str(math.floor(self.max_size/1000)) + 'кб)'
            )
        if image_w > self.max_w:
            raise ValidationError(
                'Превышена максимальная ширина изображения. ('
                + str(image_w) + 'px при допустимых ' + str(self.max_w) + 'px)'
            )
        if image_h > self.max_h:
            raise ValidationError(
                'Превышена максимальная высота изображения. ('
                + str(image_h) + 'px при допустимых ' + str(self.max_h) + 'px)'
            )

    def delete_current_avatar(self):
        """ Removes existing same-named avatar. """

        self.get_request_user()
        storage, path = self.user.avatar.storage, self.user.avatar.path
        if self.image.name in path:
            storage.delete(path)

    def generate_avatar_name(self):

        self.image_ext = self.image.content_type.split('/')[1]
        self.image.name = 'avatar.' + self.image_ext

