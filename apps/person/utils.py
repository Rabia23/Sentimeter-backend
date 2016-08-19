from apps import constants
from apps.person.enum import UserGenderEnum
from apps.person.models import UserInfo
from apps.person.serializers import UserSerializer, UserInfoSerializer
from apps.utils import save, generate_username, generate_password, make_request
from datetime import datetime

__author__ = 'aamish'


def user_get(object_id):
    response = make_request('GET', "application/json", '/1/classes/User/%s' % object_id, '')
    return response


def get_related_user(data):

    data['username'] = generate_username()
    data['password'] = generate_password()

    if "dob" in data:
        dob = data["dob"].split("-")
        date_of_birth = "2000-"+dob[1]+"-"+dob[0]
        b_day = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        data['date_of_birth'] = b_day

    user_serializer = UserSerializer(data=data)
    user = save(user_serializer)

    if user:
        data['user'] = user.id

        user_info_serializer = UserInfoSerializer(data=data)
        save(user_info_serializer)

        return user
    return None


def generate_gender_division(feedback):
    gender_groups = []
    for gender in UserGenderEnum.items():
        gender_group_feedback = feedback.filter(user__info__gender=gender[1])
        gender_groups.append({
            "gender_group_id": gender[1],
            "gender_group_label": UserGenderEnum.label(gender[0]),
            "count": gender_group_feedback.count(),
            "color_code": constants.COLORS_CUSTOMER_GENDERS[gender[1]],
        })
    return gender_groups