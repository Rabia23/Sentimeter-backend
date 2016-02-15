__author__ = 'aamish'

#------------ Triggers ------------
TRIGGER_BEFORE_SAVE = "beforeSave"
TRIGGER_AFTER_SAVE = "afterSave"

#------------ Password for Customers -------------
CUSTOMER_PASSWORD = "customerpassword"

#------------ Question Types -------------
TYPE_1 = 1
TYPE_2 = 2
TYPE_3 = 3

#------------ Feedback Analysis -------------
REGIONAL_ANALYSIS = '1'
CITY_ANALYSIS = '2'
BRANCH_ANALYSIS = '3'
AREA_ANALYSIS = '3'

DAILY_ANALYSIS = '1'
WEEK_ANALYSIS = '2'
MONTHLY_ANALYSIS = '3'
YEARLY_ANALYSIS = '4'

#------------ Day wise Data Ratting -------------
NO_OF_DAYS = 7
NO_OF_WEEKS = 7
NO_OF_MONTHS = 7
NO_OF_YEARS = 7

#------------ DAYS Option Ratting -------------
WEEKLY_DAYS_COUNT = 49
MONTHLY_DAYS_COUNT = 210
YEARLY_DAYS_COUNT = 2555

#------------ Negative Feedback -------------
NEGATIVE_SCORE_LIST = [1,2]
POSITIVE_SCORE_LIST = [3,4]
VERY_BAD_SCORE = 1
BAD_SCORE = 2

#------------ Email Constants -------------
NEGATIVE_FEEDBACK_SUBJECT = "LiveFeed | Negative Feedback Received"

#------------ Feedback Constants -------------
FEEDBACKS_PER_PAGE = 25
COMMENTS_PER_PAGE = 20

#------------ User Constants -------------
ANONYMOUS_TEXT = "Anonymous"
NOT_ATTEMPTED_TEXT = "N/A"

#------------ Branch Constants -------------
#BRANCH_FEEDBACK_TARGET = 200
BRANCH_FEEDBACK_TARGET = 10


#------------ Segment Constants -------------
STARTING_TIME = "06:00"
BREAKFAST_TIME = "11:00"
LUNCH_TIME = "15:00"
SNACK_TIME = "19:00"
DINNER_TIME = "23:00"
LATE_NIGHT_TIME = "06:00"

segments = {
    "11:00": "Breakfast",
    "15:00": "Lunch",
    "19:00": "Snack",
    "23:00": "Dinner",
    "06:00": "Late Night",
}

#------------ Shift Constants -------------
BREAKFAST_SHIFT_TIME = "11:00"
OPEN_SHIFT_TIME = "19:00"
CLOSE_SHIFT_TIME = "02:00"
OVERNIGHT_SHIFT_TIME = "06:00"

shifts = {
    "11:00": "Breakfast",
    "19:00": "Open",
    "02:00": "Close",
    "06:00": "Overnight",
}

#------------ Date Format Constants -------------
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
ONLY_DATE_FORMAT = "%Y-%m-%d"
ONLY_DATE_FORMAT_02 = "%d-%m-%y"
TIME_FORMAT = "%H:%M:%S"

#------------ Action Constants -------------
PROCESSED = 2
UNPROCESSED = 1
DEFERRED = 3

#------------ General Constants -----------------
TEXT_ALREADY_EXISTS = "Already Exists"
TEXT_DOES_NOT_EXISTS = "Does Not Exists"
TEXT_OPERATION_UNSUCCESSFUL = "Operation Unsuccessful"