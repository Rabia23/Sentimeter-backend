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


class SegmentEnum(enum.Enum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    NIGHT = 4
    LATE_NIGHT = 5

    labels = {
        MORNING: "Morning",
        AFTERNOON: "Afternoon",
        EVENING: "Evening",
        NIGHT: "Night",
        LATE_NIGHT: "Late Night"
    }

