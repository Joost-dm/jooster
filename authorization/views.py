""" Forum views."""

import redis
from rest_framework.authtoken.models import Token
from redis.exceptions import ResponseError
import json
from django.core.files.images import get_image_dimensions
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authorization import serializers
from authorization.models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from main.settings import REDIS_SETTINGS

User = get_user_model()


# todo PERMISSIONS!!!
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """User's profile details view"""

    lookup_url_kwarg = 'id'
    serializer_class = serializers.UserDetailSerializer
    queryset = CustomUser.objects.all()


class SetAvatar(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
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
            # user.avatar_url = user.avatar.path
            user.save()
            return user
        except ValidationError:
            return CustomUser.objects.get(user_id=request.user.id)


class UsersOnline(APIView):
    serializer_class = serializers.UsersOnlineSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'delete']

    users_online = redis.StrictRedis(
        host=REDIS_SETTINGS['users_online']['HOST'],
        port=REDIS_SETTINGS['users_online']['PORT'],
        db=REDIS_SETTINGS['users_online']['DB'],
        password=REDIS_SETTINGS['users_online']['PASSWORD'],
        decode_responses=True
    )

    def get(self, request):
        users = self.users_online.keys()
        users_list = []
        for user in users:
            users_list.append(CustomUser.objects.get(displayed=user))
        users_list = serializers.UsersOnlineSerializer({'users_online': users_list}).data
        return Response(users_list)

    def delete(self, request):
        auth_token = request.headers['Authorization'].split(' ')[1]
        user = Token.objects.get(key=auth_token).user
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(self.users_online.keys())
        self.users_online.delete(user.displayed)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(self.users_online.keys())
        self.get(request)
