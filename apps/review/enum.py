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
    LUNCH = 2
    EARLY_DINNER = 3
    MID_DINNER = 4
    DINNER = 5

    labels = {

        LUNCH: "Lunch",
        EARLY_DINNER: "Early Dinner",
        MID_DINNER: "Mid Dinner",
        DINNER: "Dinner"
    }
