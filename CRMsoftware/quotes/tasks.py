from celery import Celery
from django.core.mail import send_mail
from .models import Email
from django.contrib.auth import get_user_model
from django.conf import settings

app = Celery('celery_tasks', broker='pyamqp://guest@localhost//', backend='rpc://',)


@app.task
def send_email(plain_message, email_sender1, to, html_message):
    try:

        send_mail(subject='فاکتور خرید', message=plain_message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=to, html_message=html_message)

        Email.objects.create(email_sender=get_user_model().objects.get(username=email_sender1), email_receiver=to, status='True')
        return 'شد'

    except:
        Email.objects.create(email_sender=get_user_model().objects.get(username=email_sender1), email_receiver=to, status='False')
        return 'نشد'
