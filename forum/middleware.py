""" Forum middleware. """

import time
from django.contrib.auth.models import AbstractUser
from djoser.urls import authtoken

from authorization.models import CustomUser
from main import settings


class ResponseTimeCounter:
    """ Response time counter. """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #auth_token = request.headers['Authorization'].split(' ')[1]
        #print(dir(request))
        time_start = time.time()
        response = self.get_response(request)
        time_end = time.time()
        time_delta = time_end - time_start
        print('Elapsed time: ' + str(time_delta)[0:7])
        return response

