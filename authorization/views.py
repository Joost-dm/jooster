""" Forum views."""

import redis
from rest_framework.authtoken.models import Token
from django.core.files.images import get_image_dimensions
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authorization import serializers
from authorization.models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from main.tasks import send_activity_report

from main.settings import REDIS_SETTINGS

User = get_user_model()


class UsersOnline(APIView):
    """ Users online view. """

    serializer_class = serializers.UsersOnlineSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'delete']

    users_online = redis.StrictRedis(
        host=REDIS_SETTINGS['HOST'],
        port=REDIS_SETTINGS['PORT'],
        db=REDIS_SETTINGS['USERS_ONLINE_DB'],
        password=REDIS_SETTINGS['PASSWORD'],
        decode_responses=True
    )

    def get(self, request):
        try:
            self.users_online.set(request.user.displayed, 'online', ex=REDIS_SETTINGS['SESSION_LENGTH'])
        except AttributeError:
            pass
        users = self.users_online.keys()
        users_list = []
        for user in users:
            users_list.append(CustomUser.objects.get(displayed=user))
        users_list = serializers.UsersOnlineSerializer({'users_online': users_list}).data
        return Response(users_list)

    def delete(self, request):
        auth_token = request.headers['Authorization'].split(' ')[1]
        user = Token.objects.get(key=auth_token).user
        send_activity_report(user.displayed)
        self.users_online.delete(user.displayed)
        return Response(data={"users_online": "logged out."}, status=status.HTTP_200_OK)
