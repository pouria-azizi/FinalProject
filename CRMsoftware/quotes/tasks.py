from celery import Celery
from django.core.mail import send_mail

app = Celery('celery_tasks', broker='pyamqp://guest@localhost//', backend='rpc://',)


@app.task
def send_email(subject, plain_message, from_email, to, html_message):

    try:
        send_mail(subject, plain_message, from_email, [to], html_message)

        return 'شد'

    except:
        return 'نشد'
