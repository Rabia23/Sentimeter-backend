__author__ = 'aamish'

#------------ Triggers ------------
TRIGGER_BEFORE_SAVE = "beforeSave"
TRIGGER_AFTER_SAVE = "afterSave"

#------------ Password for Customers -------------
CUSTOMER_PASSWORD = "customerpassword"

#------------ Question PK -------------
PK_7 = 7

#------------ Question Types -------------
TYPE_1 = 1
TYPE_2 = 2
TYPE_3 = 3
TYPE_20 = 20
TYPE_21 = 21

#------------ Feedback Analysis -------------
REGIONAL_ANALYSIS = '1'
CITY_ANALYSIS = '2'
BRANCH_ANALYSIS = '3'
AREA_ANALYSIS = '3'
TABLE_ANALYSIS = '4'

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
FEEDBACK_REPORT_SUBJECT = "LiveFeed | Feedback Report"

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
STARTING_TIME = "01:00"
BREAKFAST_TIME = "06:00"
LUNCH_TIME = "10:00"
SNACK_TIME = "14:00"
DINNER_TIME = "18:00"
LATE_NIGHT_TIME = "01:00"

segments = {
    "06:00": "Breakfast",
    "10:00": "Lunch",
    "14:00": "Snack",
    "18:00": "Dinner",
    "01:00": "Late Night",
}

#------------ Shift Constants -------------
BREAKFAST_SHIFT_TIME = "06:00"
OPEN_SHIFT_TIME = "14:00"
CLOSE_SHIFT_TIME = "02:00"
OVERNIGHT_SHIFT_TIME = "01:00"

shifts = {
    "06:00": "Breakfast",
    "14:00": "Open",
    "02:00": "Close",
    "01:00": "Overnight",
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
TEXT_MISSING_PARAMS = "Params are missing"

#------------ Color Constants -----------------
COLORS_TOP_CONCERNS = ["#cb1e24", "#178aea", "#434347", "#f1d400", "#90ec7c"]
COLORS_ACTION_STATUS = ["#ffffff", "#cb1e24", "#ffd200", "#01c211", "#01c211"]
COLORS_CUSTOMER_GENDERS = ["#26AAE2", "#F174AC"]
