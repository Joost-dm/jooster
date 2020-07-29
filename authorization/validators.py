import math
from django.core.files.images import get_image_dimensions
from rest_framework.exceptions import ValidationError
from main.settings import USER_SETTINGS

AVATAR_SETTINGS = USER_SETTINGS['USER_AVATAR_SETTINGS']


class DownloadedAvatarValidator(object):
    """ Validation class for downloaded user's avatar images.
     Accords to user's avatar settings in project settings. """

    def __init__(self, image):
        self.max_w = AVATAR_SETTINGS['MAX_WIDTH']
        self.max_h = AVATAR_SETTINGS['MAX_HEIGHT']
        self.max_size = AVATAR_SETTINGS['MAX_SIZE']

        self.image = image
        self.validate_image()

    def __call__(self, image):
        self.image = image
        self.validate_image()

    def validate_image(self):
        """ Validator."""

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
