""" Celery tasks. """

import redis
from django.core.mail import  EmailMessage
import datetime

from .celery import app
from .settings import REDIS_SETTINGS

users_online = redis.StrictRedis(
    host=REDIS_SETTINGS['HOST'],
    port=REDIS_SETTINGS['PORT'],
    db=REDIS_SETTINGS['USERS_ONLINE_DB'],
    password=REDIS_SETTINGS['PASSWORD'],
    decode_responses=True
)
celery_broker = redis.StrictRedis(
    host=REDIS_SETTINGS['HOST'],
    port=REDIS_SETTINGS['PORT'],
    db=REDIS_SETTINGS['CELERY_BROKER_DB'],
    password=REDIS_SETTINGS['PASSWORD'],
    decode_responses=True
)


@app.task()
def check_activity():
    """ Checking fot user's session finish. """

    users_online_list = users_online.keys()

    try:
        users_log_list = celery_broker.get('users_online_log').split(',')
    except AttributeError:
        users_log_list = []

    for user in users_log_list:
        if user not in users_online_list:
            send_activity_report(user)
            print('Пользователь ' + user + ' вышел. ')
    celery_broker.set('users_online_log', ','.join(users_online_list))
    return 'Activity checked'


def send_activity_report(username):
    """ Sends a report about user's activity to my e-mail. """

    key = username + '_activity'
    user_session_activity = str(celery_broker.get(key)).split(' | ')

    if user_session_activity[0] != 'None':
        email_subject = username + ': отчёт об активности.'
        email_answer_html = '<body style="background-color: #2C3138; color: white"> ' \
                            '[' + datetime.datetime.now().strftime("%d%b, %H:%M:%S") + '] Активность пользователя ' +\
                            username + ':' + \
                            '<ol>' + \
                            '<li style="color: white;"> ' + \
                            '<li style="color: white;"> '.join(user_session_activity) + \
                            '</ol>' +\
                            '</body>'
        email_from = 'joost.mail@gmail.com'
        email_to = ['vasiliishirokov@gmail.com']
        msg = EmailMessage(email_subject, email_answer_html, email_from, email_to)
        msg.content_subtype = "html"
        msg.send()
        celery_broker.delete(key)
