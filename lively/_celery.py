from apps.person.enum import UserRolesEnum
from apps.person.models import UserInfo

__author__ = 'aamish'

import os
from celery import Celery
from django.contrib.auth.models import User
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import get_template
from lively import settings as lively_settings
from apps import constants
from celery import shared_task
from django.template import Context

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lively.settings')

from django.conf import settings

app = Celery('lively')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def send_negative_feedback_email(feedback_json):
    context = Context({'feedback': feedback_json})
    text_template = get_template('emails/negative_feedback.txt')
    html_template = get_template('emails/negative_feedback.html')

    recipients = get_recipients(feedback_json["branch_id"])
    send_mail(constants.NEGATIVE_FEEDBACK_SUBJECT, context, recipients, text_template, html_template)


def send_mail(subject, context, recipients, text_template, html_template):
    if recipients:
        email_addresses = [recipient["email"] for recipient in recipients]
        email_addresses + get_super_recipients()
        subject, from_email, to = subject, lively_settings.DEFAULT_FROM_EMAIL, email_addresses
        text_content = text_template.render(context)
        html_content = html_template.render(context)
        message = EmailMultiAlternatives(subject, text_content, from_email, to)
        message.attach_alternative(html_content, "text/html")
        message.send()


def get_recipients(branch_id):
    recipients = []
    branch_manager = UserInfo.get_person_dict_by_branch(UserRolesEnum.BRANCH_MANAGER, branch_id)
    operational_consultant = UserInfo.get_person_dict(UserRolesEnum.OPERATIONAL_CONSULTANT, branch_manager["parent"]["id"]) if branch_manager else None
    # operational_manager = UserInfo.get_person_dict(UserRolesEnum.OPERATIONAL_MANAGER, operational_consultant["parent"]["id"]) if operational_consultant else None
    # assistant_director = UserInfo.get_person_dict(UserRolesEnum.ASSISTANT_DIRECTOR, operational_manager["parent"]["id"]) if operational_manager else None
    # director = UserInfo.get_person_dict(UserRolesEnum.DIRECTOR, assistant_director["parent"]["id"]) if assistant_director else None

    # director_tier_management = UserInfo.get_people_dict(UserRolesEnum.DIRECTOR)
    # assistant_director_tier_management = UserInfo.get_people_dict(UserRolesEnum.ASSISTANT_DIRECTOR)

    recipients.append(branch_manager)
    recipients.append(operational_consultant)
    # recipients.append(operational_manager)

    # [recipients.append(director) for director in director_tier_management]
    # [recipients.append(assistant_director) for assistant_director in assistant_director_tier_management]

    return recipients


def get_super_recipients():
    recipients = []
    superusers = User.objects.filter(is_superuser=True)
    for superuser in superusers:
        recipients.append(superuser.email)
    return recipients


@shared_task
def send_feedback_email_report(feedback_json):
    context = Context({'feedback': feedback_json})
    text_template = get_template('emails/feedback_email_report.txt')
    html_template = get_template('emails/feedback_email_report.html')

    recipients = get_upper_management_recipients()
    send_mail(constants.FEEDBACK_REPORT_SUBJECT, context, recipients, text_template, html_template)


def get_upper_management_recipients():
    recipients = []

    director_tier_management = UserInfo.get_people_dict(UserRolesEnum.DIRECTOR)
    assistant_director_tier_management = UserInfo.get_people_dict(UserRolesEnum.ASSISTANT_DIRECTOR)
    operational_manager_tier_management = UserInfo.get_people_dict(UserRolesEnum.OPERATIONAL_MANAGER)

    [recipients.append(director) for director in director_tier_management]
    [recipients.append(assistant_director) for assistant_director in assistant_director_tier_management]
    [recipients.append(operational_manager) for operational_manager in operational_manager_tier_management]

    return recipients