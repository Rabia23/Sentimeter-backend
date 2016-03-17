__author__ = 'aamish'
from django_enumfield import enum


class UserRolesEnum(enum.Enum):
    CUSTOMER = 1
    GRO = 2
    BRANCH_MANAGER = 3
    OPERATIONAL_CONSULTANT = 4
    OPERATIONAL_MANAGER = 5
    ASSISTANT_DIRECTOR = 6
    DIRECTOR = 7

    labels = {
        CUSTOMER: 'CUSTOMER',
        GRO: 'GRO',
        BRANCH_MANAGER: 'BRANCH_MANAGER',
        OPERATIONAL_CONSULTANT: 'OPERATIONAL_CONSULTANT',
        OPERATIONAL_MANAGER: 'OPERATIONAL_MANAGER',
        ASSISTANT_DIRECTOR: 'ASSISTANT_DIRECTOR',
        DIRECTOR: 'DIRECTOR'
    }


class UserGenderEnum(enum.Enum):
    MALE = 0
    FEMALE = 1

    labels = {
        MALE: 'MALE',
        FEMALE: 'FEMALE',
    }


class UserAgeEnum(enum.Enum):
    BELOW18 = 0
    BETWEEN18TO30 = 1
    BETWEEN31TO44 = 2
    BETWEEN45TO54 = 3
    BETWEEN55TO64 = 4
    ABOVE65 = 5

    labels = {
        BELOW18: 'Below 18',
        BETWEEN18TO30: '18-30',
        BETWEEN31TO44: '31-44',
        BETWEEN45TO54: '45-54',
        BETWEEN55TO64: '55-64',
        ABOVE65: '65 Above'
    }