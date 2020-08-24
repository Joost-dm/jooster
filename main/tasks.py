from django.core.mail import send_mail
import datetime

from .celery import app


@app.task()
def check_activity():
    send_mail('Дата', 'Время: ' + str(datetime.datetime.now()),
              'joost.mail@gmail.com', ['vasiliishirokov@gmail.com'], fail_silently=False)
    return 'Done'
