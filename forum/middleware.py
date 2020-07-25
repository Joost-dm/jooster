""" Forum middleware. """
import time

class ResponseTimeCounter:
    """ Response time counter. """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_start = time.time()
        response = self.get_response(request)
        time_end = time.time()
        time_delta = time_end - time_start
        print('Elapsed time: ' + str(time_delta)[0:7])
        return response

