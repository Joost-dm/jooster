""" Forum views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.images import get_image_dimensions
from django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from djoser.serializers import UserCreateSerializer

from authorization import serializers
from authorization.models import CustomUser


from django.contrib.auth import  get_user_model
from rest_framework.exceptions import ValidationError

from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings

from forum import permissions

User = get_user_model()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """User's profile details view"""

    lookup_url_kwarg = 'id'
    serializer_class = serializers.UserDetailSerializer
    queryset = CustomUser.objects.all()

#todo delete?
def create(self, validated_data):
    try:
        user = self.perform_create(validated_data)
    except IntegrityError:
        self.fail("cannot_create_user")

    return user

UserCreateSerializer.create= create

class SetAvatar(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        print('dddd')
        # Получение изображения.
        image = request.FILES['avatar']
        try:
            # Валидация ширины и высоты изображения.
            image_w, image_h = get_image_dimensions(image)
            if image_w > 600 or image_h > 600:
                raise ValidationError(detail='Размер изображения не должен превышать 600х600px', code='400')
            # Удаления старого аватара и установка нового.
            user = CustomUser.objects.get(user_id=request.user.id)
            storage, path = user.avatar.storage, user.avatar.path
            if "users" in path:
                storage.delete(path)
            user.avatar = image
            user.save()
            return user
        except ValidationError:
            return CustomUser.objects.get(user_id=request.user.id)
