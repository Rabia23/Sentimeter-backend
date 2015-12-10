from django.contrib.auth.models import User
from django.db import models
from app.models import Branch, UserInfo
from lively import constants, settings
from datetime import datetime
from dateutil import tz


class Feedback(models.Model):
    user = models.ForeignKey(User, related_name='feedback', null=True, blank=True)
    branch = models.ForeignKey(Branch, related_name='feedback', null=True, blank=True)
    comment = models.CharField(max_length=1000)
    objectId = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    action_taken = models.IntegerField(default=constants.UNPROCESSED)

    def __str__(self):
       return self.objectId

    @staticmethod
    def get_if_exists(objectId):
        feedback = Feedback.objects.filter(objectId=objectId).first()
        if feedback:
            return feedback

    def is_negative(self):
        options = self.feedback_option.filter(option__score__in=constants.NEGATIVE_SCORE_LIST)
        if options:
            return True
        return False

    def is_bad(self):
        options = self.feedback_option.filter(option__score=constants.BAD_SCORE)
        if options:
            return True
        return False

    def problems(self):
        problems = self.feedback_option.all().exclude(option__parent=None).values("option__text")
        return ", ".join(problem["option__text"] for problem in problems)

    def customer_name(self):
        if self.user:
            if self.user.first_name:
                return self.user.first_name
        return constants.ANONYMOUS_TEXT

    def customer_phone(self):
        user_info = UserInfo.objects.filter(user=self.user).first()
        if user_info:
            if user_info.phone_no:
                return user_info.phone_no
        return constants.NOT_ATTEMPTED_TEXT

    def selected_main_option(self):
        main_question = Question.objects.get(type=constants.MAIN_QUESTION)
        option_list = self.feedback_option.filter(option__in=main_question.options.filter().values_list('id')).values_list('option_id')
        option = Option.objects.filter(pk__in=option_list).first()
        if option:
            return option

    def selected_secondary_option(self):
        secondary_question = Question.objects.get(type=constants.SECONDARY_QUESTION)
        option_list = self.feedback_option.filter(option__in=secondary_question.options.filter().values_list('id')).values_list('option_id')
        options = Option.objects.filter(pk__in=option_list)
        if options:
            return options

    def get_segment(self):
        start_time = get_time(constants.STARTING_TIME)
        breakfast_time = get_time(constants.BREAKFAST_TIME)
        lunch_time = get_time(constants.LUNCH_TIME)
        snack_time = get_time(constants.SNACK_TIME)
        dinner_time = get_time(constants.DINNER_TIME)
        late_night_time = get_time(constants.LATE_NIGHT_TIME)

        created_at = get_converted_time(self.created_at)

        if created_at >= start_time and created_at < breakfast_time:
            return constants.segments[constants.BREAKFAST_TIME]
        elif created_at >= breakfast_time and created_at < lunch_time:
            return constants.segments[constants.LUNCH_TIME]
        elif created_at >= lunch_time and created_at < snack_time:
            return constants.segments[constants.SNACK_TIME]
        elif created_at >= snack_time and created_at < dinner_time:
            return constants.segments[constants.DINNER_TIME]
        elif created_at >= dinner_time and created_at < late_night_time:
            return constants.segments[constants.LATE_NIGHT_TIME]
        return ""

    def get_shift(self):
        start_time = get_time(constants.STARTING_TIME)
        breakfast_shift = get_time(constants.BREAKFAST_SHIFT_TIME)
        open_shift = get_time(constants.OPEN_SHIFT_TIME)
        close_shift = get_time(constants.CLOSE_SHIFT_TIME)
        over_night_shift = get_time(constants.OVERNIGHT_SHIFT_TIME)

        created_at = get_converted_time(self.created_at)

        if created_at >= start_time and created_at < breakfast_shift:
            return constants.shifts[constants.BREAKFAST_TIME]
        elif created_at >= breakfast_shift and created_at < open_shift:
            return constants.shifts[constants.OPEN_SHIFT_TIME]
        elif created_at >= open_shift and created_at < close_shift:
            return constants.shifts[constants.CLOSE_SHIFT_TIME]
        elif created_at >= close_shift and created_at < over_night_shift:
            return constants.shifts[constants.OVERNIGHT_SHIFT_TIME]
        return ""

    def to_dict(self):
        try:
            feedback = {
                "objectId": self.objectId,
                "comment": self.comment,
                "branch": self.branch.name,
                "city": self.branch.city.name,
                "region": self.branch.city.region.name,
                "main_question_options": self.selected_main_option(),
                "secondary_question_options": self.selected_secondary_option(),
            }
            return feedback
        except Exception as e:
            return {}

    def feedback_comment_dict(self):
        user_info = UserInfo.objects.filter(user=self.user).first()
        try:
            feedback = {
                "id": self.id,
                "objectId": self.objectId,
                "comment": self.comment,
                "branch": self.branch.name,
                "city": self.branch.city.name,
                "region": self.branch.city.region.name,
                "user_name": user_info.get_username() if user_info else None,
                "user_phone": user_info.get_phone() if user_info else None,
                "segment": self.get_segment(),
                "shift": self.get_shift(),
                "is_negative": self.is_negative(),
                "action_taken": self.action_taken,
            }
            return feedback
        except Exception as e:
            return {}


class Question(models.Model):
    text = models.TextField()
    isActive = models.BooleanField(default=True)
    type = models.IntegerField()
    objectId = models.CharField(max_length=20)

    def __str__(self):
       return self.text

    @staticmethod
    def get_if_exists(objectId):
        question = Question.objects.filter(objectId=objectId).first()
        if question:
            return question


class Option(models.Model):
    text = models.TextField()
    objectId = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    question = models.ForeignKey(Question, related_name='options', null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
       return self.text

    @staticmethod
    def get_if_exists(objectId):
        option = Option.objects.filter(objectId=objectId).first()
        if option:
            return option

    def is_parent(self):
        return self.children.count() > 0


class FeedbackOption(models.Model):
    objectId = models.CharField(max_length=20)
    feedback = models.ForeignKey(Feedback, related_name='feedback_option', null=True, blank=True)
    option = models.ForeignKey(Option, related_name='feedback_option', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_option_dict(self):
        try:
            feedback_option = {
                "option_id": self.option_id,
                "option__text": self.option.text,
            }
            return feedback_option
        except Exception as e:
            return {}

    def is_negative_option(self):
        if self.option.score in constants.NEGATIVE_SCORE_LIST:
            return True
        return False

    def __str__(self):
       return self.objectId

    @staticmethod
    def get_if_exists(objectId):
        feedback_option = FeedbackOption.objects.filter(objectId=objectId).first()
        if feedback_option:
            return feedback_option


def get_time(constant):
    return datetime.strptime(constant, '%H:%M').time()


def get_converted_time(time):
    time = time.strftime(constants.DATE_FORMAT)

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Karachi')
    utc = datetime.strptime(str(time), constants.DATE_FORMAT)
    utc = utc.replace(tzinfo=from_zone)
    converted_time = utc.astimezone(to_zone)
    return converted_time.time()
