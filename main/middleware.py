import redis
import time
from datetime import datetime

from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

from main.settings import REDIS_SETTINGS


class UsersOnlineChecker:
    """ Checks Users """

    def __init__(self, get_response):
        self.get_response = get_response
        self.users_online = redis.StrictRedis(
            host=REDIS_SETTINGS['HOST'],
            port=REDIS_SETTINGS['PORT'],
            db=REDIS_SETTINGS['USERS_ONLINE_DB'],
            password=REDIS_SETTINGS['PASSWORD'],
            decode_responses=True
        )
        self.celery_broker = redis.StrictRedis(
            host=REDIS_SETTINGS['HOST'],
            port=REDIS_SETTINGS['PORT'],
            db=REDIS_SETTINGS['CELERY_BROKER_DB'],
            password=REDIS_SETTINGS['PASSWORD'],
            decode_responses=True
        )

    def __call__(self, request):
        try:
            auth_token = request.headers['Authorization'].split(' ')[1]
            user = Token.objects.get(key=auth_token).user
            if request.path[-7:] == 'online/' and request.method == 'DELETE':
                self.users_online.delete(user.displayed)
                response = self.get_response(request)
                print('user: ' + user.displayed + ' logged out.')
            else:
                self.users_online.set(user.displayed, 'online', ex=REDIS_SETTINGS['SESSION_LENGTH'])
                response = self.get_response(request)
                self.log_user_activity(request, user, response)
                print('user: ' + user.displayed)
        except (ObjectDoesNotExist, KeyError, TypeError):
            print('Unknown user.')
            allowed_paths = [
                '/api/v1/auth/token/login/',
                '/api/v1/auth/online/',
                '/api/v1/auth/users/'
            ]
            if request.path.startswith('/api/v1/') and request.path not in allowed_paths:
                return JsonResponse({'user': 'Not Authorized.'}, status=status.HTTP_401_UNAUTHORIZED)
            response = self.get_response(request)
        return response

    def log_user_activity(self, request, user, response):
        """ Logs user's action. """

        user = user.displayed
        activity = '[' + datetime.now().strftime("%d%b, %H:%M:%S") + '] ' \
                   'RESPONSE CODE: ' + str(response.status_code) + ' ' + \
                   'REQUEST:  ' + request.method + ' => ' + request.path
        key = user + '_activity'

        activity_log = str(self.celery_broker.get(key))
        if activity_log != 'None':
            total_activity = activity_log + ' | ' + activity
        else:
            total_activity = activity
        self.celery_broker.set(key, total_activity)


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
