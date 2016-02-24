__author__ = 'aamish'
from django_enumfield import enum


class ActionStatusEnum(enum.Enum):
    UNPORCESSED = 1
    UNRECOVERABLE = 2
    RECOVERED = 3
    NOACTIONNEEDED = 4

    labels = {
        UNPORCESSED: "Unprocessed",
        UNRECOVERABLE: "Unrecoverable",
        RECOVERED: "Recovered",
        NOACTIONNEEDED: "No Action Needed"
    }