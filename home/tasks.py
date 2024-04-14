from celery import shared_task
from django.core.mail import send_mail
from .models import Subscriber
from django.template.loader import render_to_string
from .views import trending_api
from concurrent.futures import ThreadPoolExecutor


def send_email(email_address, html_message):
    send_mail(subject="Your Daily Dose of Headlines: Top 10 Stories You Need to Know",
              message="",
              from_email='TazaKhabre @admin',
              recipient_list=[email_address],
              html_message=html_message)


@shared_task(name='sending_emails_to_subscribers', ignore_result=True)
def sending_emails_to_subscribers():
    response = trending_api(params={'country': 'in',
                                    'category': 'general',
                                    'page': 1,
                                    'pageSize': 10})

    html_message = render_to_string('mail_template.html', context={'articles': response['articles']})
    with ThreadPoolExecutor() as executor:
        for sub in Subscriber.objects.all():
            executor.submit(send_email, sub.email, html_message)