import redis
import time
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from main.settings import REDIS_SETTINGS

class UsersOnlineChecker:
    """ Checks Users """

    def __init__(self, get_response):
        self.get_response = get_response
        self.users_online = redis.StrictRedis(
            host=REDIS_SETTINGS['users_online']['HOST'],
            port=REDIS_SETTINGS['users_online']['PORT'],
            db=REDIS_SETTINGS['users_online']['DB'],
            password=REDIS_SETTINGS['users_online']['PASSWORD'],
            decode_responses=True
        )

    def __call__(self, request):
        response = self.get_response(request)
        try:
            auth_token = request.headers['Authorization'].split(' ')[1]
            user = Token.objects.get(key=auth_token).user
            self.users_online.set(user.displayed, 'online', ex=REDIS_SETTINGS['users_online']['SESSION_LENGTH'])
            print('user: ' + user.displayed)
        except (ObjectDoesNotExist, KeyError):
            print('unknown user')
        return response


class ResponseTimeCounter:
    """ Response time counter. """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_start = time.time()
        response = self.get_response(request)
        time_end = time.time()
        time_delta = time_end - time_start
        print('elapsed time: ' + str(time_delta)[0:7])
        return response
