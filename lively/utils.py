from django.contrib.auth.models import User
from app.models import Region, City, Branch, UserInfo
from app.serializers import RegionSerializer, CitySerializer, BranchSerializer, UserSerializer, UserInfoSerializer
from rest_framework import status
from rest_framework.response import Response
from feedback.models import Feedback, Option
from feedback.serializers import FeedbackSerializer, OptionSerializer
from lively import constants, settings
import string,random
from lively.parse_utils import region_get, feedback_get, option_get
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


__author__ = 'aamish'

#**************** Generic Util Methods ****************


def save_and_response(serializer, data):
    if serializer.is_valid():
        serializer.save()
        data = {
            "success": data
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def save(serializer):
    if serializer.is_valid():
        return serializer.save()


def response(data):
    data = {
        "success": data
    }
    return Response(data, status=status.HTTP_200_OK)

#**************** Related Objects Methods ****************
#all need to be refactored -  can be converted into one method


def get_related_region(data):
    region = Region.get_if_exists(data["objectId"])
    if region:
        serializer = RegionSerializer(region, data=data)
    else:
        serializer = RegionSerializer(data=data)

    if serializer.is_valid():
        region = serializer.save()
        return region


def get_related_city(data):
    city = City.get_if_exists(data["objectId"])
    if city:
        serializer = CitySerializer(city, data=data)
    else:
        serializer = CitySerializer(data=data)

    if serializer.is_valid():
        city = serializer.save()

        #will use this after testing the nested example otherwise will remove this code
        # related_region = region_get(data["region"]["objectId"])
        # region = get_related_region(related_region)
        #
        # city.region = region
        # city.save()

        return city


def get_related_branch(data):
    branch = Branch.get_if_exists(data["objectId"])
    if branch:
        serializer = BranchSerializer(branch, data=data)
    else:
        serializer = BranchSerializer(data=data)

    if serializer.is_valid():
        branch = serializer.save()
        return branch


def get_related_user(data):
    user_info = UserInfo.get_if_exists(data["objectId"])
    if user_info:
        user_info_serializer = UserInfoSerializer(user_info, data=data)
        user_serializer = UserSerializer(user_info.user, data=data)

        save(user_info_serializer)
        user = save(user_serializer)
        return user
    else:
        data['username'] = generate_username()
        data['password'] = constants.CUSTOMER_PASSWORD

        user_info_serializer = UserInfoSerializer(data=data)
        user_info = save(user_info_serializer)

        if user_info:
            user_serializer = UserSerializer(data=data)
            user = save(user_serializer)

            return associate_info_to_user(user, user_info)


def associate_info_to_user(user, user_info):
    if user:
        user_info.user = user
        user_info.save()

        return user
    else:
        user_info.delete()


def get_related_option(data):
    option = Option.get_if_exists(data["objectId"])
    if option:
        serializer = OptionSerializer(option, data=data)
    else:
        serializer = OptionSerializer(data=data)

    if serializer.is_valid():
        option = serializer.save()

        if "subOptions" in data:
            for sub_option_data in data["subOptions"]:
                sub_option_parse = option_get(sub_option_data["objectId"])
                sub_option = get_related_option(sub_option_parse)

                sub_option.parent = option
                sub_option.save()

        return option


def get_related_feedback(data):
    feedback = Feedback.get_if_exists(data["objectId"])
    if feedback:
        serializer = FeedbackSerializer(feedback, data=data)
    else:
        serializer = FeedbackSerializer(data=data)

    if serializer.is_valid():
        feedback = serializer.save()
        return feedback


#copied
def generate_username():
    # Python 3 uses ascii_letters. If not available, fallback to letters
    try:
        letters = string.ascii_letters
    except AttributeError:
        letters = string.letters
    uname = ''.join([random.choice(letters + string.digits + '_')
                     for i in range(30)])
    try:
        User.objects.get(username=uname)
        return generate_username()
    except User.DoesNotExist:
        return uname


def generate_missing_options(question, data):
    list_feedback_option_ids = [item['option_id'] for item in data]
    list_feedback = list(data)

    for option in question.options.all():
        if option.id not in list_feedback_option_ids:
            list_feedback.append({'count': 0,
                                  'option_id': option.id,
                                  'option__text': option.text,
                                  'option__parent_id': option.parent_id})

    return list_feedback


def generate_missing_sub_options(option_id, data):
    list_feedback_option_ids = [item['option_id'] for item in data]
    list_feedback = list(data)

    for option in Option.objects.filter(parent=option_id):
        if option.id not in list_feedback_option_ids:
            list_feedback.append({'count': 0,
                                  'option_id': option.id,
                                  'option__text': option.text,
                                  'option__parent_id': option.parent_id})

    return list_feedback


def get_filtered_feedback_options(feedback_options, type, object):
    if type == constants.CITY_ANALYSIS:
        filtered_feedback_options = feedback_options.filter(feedback__branch__city__exact=object.id)
    elif type == constants.BRANCH_ANALYSIS:
        filtered_feedback_options = feedback_options.filter(feedback__branch__exact=object.id)
    else:
        filtered_feedback_options = feedback_options.filter(feedback__branch__city__region__exact=object.id)

    return filtered_feedback_options


def send_negative_feedback_email(context):
    text_template = get_template('emails/negative_feedback.txt')
    html_template = get_template('emails/negative_feedback.html')

    recipients = User.objects.filter(is_superuser=True)
    send_mail(constants.NEGATIVE_FEEDBACK_SUBJECT, context, recipients, text_template, html_template)


def send_mail(subject, context, recipients, text_template, html_template):
    email_addresses = [recipient.email for recipient in recipients]
    subject, from_email, to = subject, settings.DEFAULT_FROM_EMAIL, email_addresses
    text_content = text_template.render(context)
    html_content = html_template.render(context)
    message = EmailMultiAlternatives(subject, text_content, from_email, to)
    message.attach_alternative(html_content, "text/html")
    message.send()

