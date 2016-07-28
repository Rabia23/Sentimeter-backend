from django.template.loader import render_to_string
# from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.mail import get_connection
from apps.person.models import UserInfo
from apps.person.enum import UserRolesEnum
from lively import settings


def sendEmaiLMailGun(feedback_json):
    try:
        subject = 'Testing mail gun!'
        context = {'feedback': feedback_json}
        txt = render_to_string('emails/negative_feedback.html', context)
        html = render_to_string('emails/negative_feedback.html', context)
        recipients = get_recipients(1)
        # recipients = get_recipients(feedback_json["branch_id"])
        email_addresses = [recipient["email"] for recipient in recipients]
        print(email_addresses)
        send_email(subject, email_addresses, html, txt)
    except Exception as e:
        print("in exception")
        print(e)


def send_email(subject, email_addresses, html, txt):
    try:
        print("1")
        connection = get_connection('django_mailgun_mime.backends.MailgunMIMEBackend', api_key=settings.api_key, domain=settings.domain)
        print("2")
        send_mail(subject, txt, settings.DEFAULT_FROM_EMAIL, email_addresses, connection=connection, html_message=html)
        print("4")
    except Exception as e:
        print(e)


def get_recipients(branch_id):
    # recipients = []
    # branch_manager = UserInfo.get_person_dict_by_branch(UserRolesEnum.BRANCH_MANAGER, branch_id)
    # operational_consultant = UserInfo.get_person_dict(UserRolesEnum.OPERATIONAL_CONSULTANT, branch_manager["parent"]["id"]) if branch_manager else None
    # # operational_manager = UserInfo.get_person_dict(UserRolesEnum.OPERATIONAL_MANAGER, operational_consultant["parent"]["id"]) if operational_consultant else None
    # # assistant_director = UserInfo.get_person_dict(UserRolesEnum.ASSISTANT_DIRECTOR, operational_manager["parent"]["id"]) if operational_manager else None
    # # director = UserInfo.get_person_dict(UserRolesEnum.DIRECTOR, assistant_director["parent"]["id"]) if assistant_director else None
    #
    # # director_tier_management = UserInfo.get_people_dict(UserRolesEnum.DIRECTOR)
    # # assistant_director_tier_management = UserInfo.get_people_dict(UserRolesEnum.ASSISTANT_DIRECTOR)
    #
    # recipients.append(branch_manager)
    # recipients.append(operational_consultant)
    # # recipients.append(operational_manager)
    # #
    # # [recipients.append(director) for director in director_tier_management]
    # # [recipients.append(assistant_director) for assistant_director in assistant_director_tier_management]
    # return recipients
    return [{"email": "rabia.iftikhar@arbisoft.com"}, {"email": "zamanafzal@gmail.com"}]


# ------------------------- feed-back report  ---------------------------------
def sendReportMailGun(feedback_json):
    try:
        subject = 'Testing Report mail gun!'
        context = {'feedback': feedback_json}
        txt = render_to_string('emails/feedback_email_report.txt', context)
        html = render_to_string('emails/feedback_email_report.html', context)
        recipients = get_upper_management_recipients()
        # recipients = get_recipients(feedback_json["branch_id"])
        email_addresses = [recipient["email"] for recipient in recipients]
        print(email_addresses)
        send_email(subject, email_addresses, html, txt)
    except Exception as e:
        print("in exception")
        print(e)


def get_upper_management_recipients():
    # recipients = []
    #
    # director_tier_management = UserInfo.get_people_dict(UserRolesEnum.DIRECTOR)
    # assistant_director_tier_management = UserInfo.get_people_dict(UserRolesEnum.ASSISTANT_DIRECTOR)
    # operational_manager_tier_management = UserInfo.get_people_dict(UserRolesEnum.OPERATIONAL_MANAGER)
    #
    # [recipients.append(director) for director in director_tier_management]
    # [recipients.append(assistant_director) for assistant_director in assistant_director_tier_management]
    # [recipients.append(operational_manager) for operational_manager in operational_manager_tier_management]

    # return recipients
    return [{"email": "rabia.iftikhar@arbisoft.com"}, {"email": "zamanafzal@gmail.com"}]