from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Count
from apps.branch.models import Branch
from apps.city.models import City
from apps.option.models import Option
from apps.question.models import Question
from apps import constants
from datetime import datetime
from dateutil import tz
from django.utils import timezone
from apps.region.models import Region


class FeedbackQuerySet(models.QuerySet):
    def date(self, date_from, date_to):
        if date_to and date_from:
            current_tz = timezone.get_current_timezone()
            date_to = current_tz.localize(datetime.strptime(date_to + " 23:59:59", constants.DATE_FORMAT))
            date_from = current_tz.localize(datetime.strptime(date_from + " 00:00:00", constants.DATE_FORMAT))
            return self.filter(created_at__gt=date_from, created_at__lte=date_to)
        return self

    def filters(self, region_id, city_id, branch_id, area_id=None):
        if region_id and city_id and branch_id:
            return self.filter(
                branch__exact=branch_id,
                branch__city__exact=city_id,
                branch__city__region__exact=region_id)
        elif region_id and city_id:
            return self.filter(
                branch__city__exact=city_id,
                branch__city__region__exact=region_id)
        elif region_id:
            return self.filter(branch__city__region__exact=region_id)
        elif branch_id:
            return self.filter(branch__exact=branch_id)
        elif area_id:
            return self.filter(branch__city__region__area__exact=area_id)
        return self

    def related_filters(self, type, object):
        if type == constants.CITY_ANALYSIS:
            return self.filter(branch__city__exact=object.id)
        elif type == constants.BRANCH_ANALYSIS:
            return self.filter(branch__exact=object.id)
        elif type == constants.REGIONAL_ANALYSIS:
            return self.filter(branch__city__region__exact=object.id)
        else:
            return self.filter(branch__city__region__area__exact=object.id)

    def top_comments(self, comment_type):
        return self.filter(feedback_option__option__score__in=comment_type). \
                   exclude(comment__isnull=True).exclude(comment__exact='').order_by('-id')[:3]

    def comments(self):
        return self.filter(comment__isnull=False).exclude(comment__exact='').order_by('-id')

    def normal_feedback(self):
        return self.exclude(feedback_option__option__question__isPromotion=True)


class FeedbackManager(models.Manager):
    def get_query_set(self):
        return FeedbackQuerySet(Feedback)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


class Feedback(models.Model):
    comment = models.CharField(max_length=1000, db_index=True, null=True, blank=True)
    objectId = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    action_taken = models.IntegerField(default=constants.UNPROCESSED, db_index=True)
    gro_name = models.CharField(max_length=25, null=True, blank=True, db_index=True)
    gro = models.ForeignKey(User, related_name='gro', null=True, blank=True)
    user = models.ForeignKey(User, related_name='feedback', null=True, blank=True)
    branch = models.ForeignKey(Branch, related_name='feedback')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = models.Manager()
    manager = FeedbackManager()


    def __str__(self):
        return self.objectId

    @staticmethod
    def get_if_exists(objectId):
        feedback = Feedback.objects.filter(objectId=objectId).first()
        if feedback:
            return feedback

    @staticmethod
    def get_feedback_type_count(date_from=None, date_to=None):
        negative_feedback_count = Feedback.manager.date(date_from, date_to).filter(feedback_option__option__score__in=constants.NEGATIVE_SCORE_LIST).count()
        positive_feedback_count = Feedback.manager.date(date_from, date_to).filter(feedback_option__option__score__in=constants.POSITIVE_SCORE_LIST).count()

        return {"positive_feedback_count": positive_feedback_count, "negative_feedback_count": negative_feedback_count}

    @staticmethod
    def get_top_branch(date_from=None, date_to=None):
        result = None
        dict = Feedback.manager.date(date_from, date_to).values('branch_id').annotate(count=Count("branch_id"))
        if dict:
            dict = dict.latest("count")
            branch = Branch.objects.get(pk=dict["branch_id"])
            result = {"count": dict["count"], "branch_name": branch.name, "branch_id": branch.id}
        return result

    @staticmethod
    def get_top_branches(date_from=None, date_to=None):
        dict = Feedback.manager.date(date_from, date_to).values('branch_id').annotate(count=Count("branch_id")).order_by('-count')[:3]

        branch_list = []
        for branch_dict in dict:
            branch = Branch.objects.get(pk=branch_dict["branch_id"])
            branch_list.append({
                "count": branch_dict["count"],
                "branch": {"branch_name": branch.name, "branch_id": branch.id},
                "city": {"city_name": branch.city.name, "city_id": branch.city.id}
            })
        return branch_list

    @staticmethod
    def get_top_city(date_from=None, date_to=None):
        result = None
        dict = Feedback.manager.date(date_from, date_to).values('branch__city_id').annotate(count=Count("branch__city_id"))
        if dict:
            dict = dict.latest("count")
            city = City.objects.get(pk=dict["branch__city_id"])
            result = {"count": dict["count"], "city_name": city.name, "city_id": city.id}
        return result

    @staticmethod
    def get_top_gro(date_from=None, date_to=None):
        result = None
        dict = Feedback.manager.date(date_from, date_to).values('gro_id').annotate(count=Count("gro_id"))

        if dict:
            dict = dict.latest("count")
            if dict["gro_id"]:
                gro = User.objects.get(pk=dict["gro_id"])

                #this will be changed once relations between branch, gro and other role is implemented.
                branch_id = Feedback.objects.filter(gro_id=gro.id).first().branch_id
                branch = Branch.objects.get(pk=branch_id)

                result = {"count": dict["count"],
                        "gro": {"gro_name": gro.first_name + " " + gro.last_name, "gro_id": gro.id},
                        "branch": {"branch_name": branch.name, "branch_id": branch.id}}
        return result

    @staticmethod
    def get_top_region(date_from=None, date_to=None):
        result = None
        dict = Feedback.manager.date(date_from, date_to).values('branch__city__region_id').annotate(count=Count("branch__city__region_id"))

        if dict:
            dict = dict.latest("count")
            region = Region.objects.get(pk=dict["branch__city__region_id"])
            result = {"count": dict["count"], "region_name": region.name, "region_id": region.id}
        return result

    def is_negative(self):
        options = self.feedback_option.filter(option__score__in=constants.NEGATIVE_SCORE_LIST)
        if options:
            return True
        return False

    def not_empty(self):
        if ((not self.comment) or self.comment == "") and self.customer_name() == constants.ANONYMOUS_TEXT and self.customer_phone() == constants.NOT_ATTEMPTED_TEXT and self.customer_email() == constants.NOT_ATTEMPTED_TEXT:
            return False
        return True

    def keyword_analysis(self):
        if self.comment_exists() and self.is_negative():
            for concern in Concern.get_all_concerns():
                if self.comment.lower().find(concern.keyword) != -1:
                    concern.count += 1
                    concern.save()

    def comment_exists(self):
        return True if self.comment else False

    def mark_deferred_if_positive_and_no_comment(self):
        if not self.is_negative() or not self.comment_exists():
            self.action_taken = constants.DEFERRED
            self.save()

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
                if self.user.last_name:
                    return self.user.first_name + " " + self.user.last_name
                return self.user.first_name
        return constants.ANONYMOUS_TEXT

    def customer_email(self):
        if self.user:
            if self.user.email:
                return self.user.email
        return constants.NOT_ATTEMPTED_TEXT

    def customer_phone(self):
        if self.user:
            user_info = self.user.info.first()
            if user_info:
                if user_info.phone_no:
                    return user_info.phone_no
        return constants.NOT_ATTEMPTED_TEXT

    def selected_main_option(self):
        main_question = Question.objects.get(type=constants.TYPE_1)
        option_list = self.feedback_option.filter(
            option__in=main_question.options.filter().values_list('id')).values_list('option_id')
        option = Option.objects.filter(pk__in=option_list).first()
        if option:
            return option

    def selected_secondary_option(self):
        secondary_question = Question.objects.get(type=constants.TYPE_2)
        option_list = self.feedback_option.filter(
            option__in=secondary_question.options.filter().values_list('id')).values_list('option_id')
        options = Option.objects.filter(pk__in=option_list)
        if options:
            return options

    def next_day_feedback(self):
        created_at = self.created_at.time()
        dinner_time = self.get_time(constants.DINNER_TIME)
        if created_at >= dinner_time:
            return False
        return True

    def get_segment(self):
        start_time = self.get_time(constants.STARTING_TIME)
        breakfast_time = self.get_time(constants.BREAKFAST_TIME)
        lunch_time = self.get_time(constants.LUNCH_TIME)
        snack_time = self.get_time(constants.SNACK_TIME)
        dinner_time = self.get_time(constants.DINNER_TIME)
        late_night_time = self.get_time(constants.LATE_NIGHT_TIME)

        created_at = self.created_at.time()

        if created_at >= start_time and created_at < breakfast_time:
            return constants.segments[constants.BREAKFAST_TIME]
        elif created_at >= breakfast_time and created_at < lunch_time:
            return constants.segments[constants.LUNCH_TIME]
        elif created_at >= lunch_time and created_at < snack_time:
            return constants.segments[constants.SNACK_TIME]
        elif created_at >= snack_time and created_at < dinner_time:
            return constants.segments[constants.DINNER_TIME]
        elif created_at >= dinner_time:
            return constants.segments[constants.LATE_NIGHT_TIME]
        elif created_at < start_time:
            return constants.segments[constants.LATE_NIGHT_TIME]
        return ""

    def get_shift(self):
        start_time = self.get_time(constants.STARTING_TIME)
        breakfast_shift = self.get_time(constants.BREAKFAST_SHIFT_TIME)
        open_shift = self.get_time(constants.OPEN_SHIFT_TIME)
        close_shift = self.get_time(constants.CLOSE_SHIFT_TIME)
        over_night_shift = self.get_time(constants.OVERNIGHT_SHIFT_TIME)

        created_at = self.created_at.time()

        if created_at >= start_time and created_at < breakfast_shift:
            return constants.shifts[constants.BREAKFAST_TIME]
        elif created_at >= breakfast_shift and created_at < open_shift:
            return constants.shifts[constants.OPEN_SHIFT_TIME]
        elif created_at >= open_shift and created_at < close_shift:
            return constants.shifts[constants.CLOSE_SHIFT_TIME]
        elif created_at >= close_shift:
            return constants.shifts[constants.OVERNIGHT_SHIFT_TIME]
        elif created_at < start_time:
            return constants.shifts[constants.OVERNIGHT_SHIFT_TIME]
        return ""

    def get_time(self, constant):
        return datetime.strptime(constant, '%H:%M').time()

    def get_converted_time(self, time):

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Karachi')
        utc = datetime.strptime(str(time), constants.DATE_FORMAT)
        utc = utc.replace(tzinfo=from_zone)
        converted_time = utc.astimezone(to_zone)
        return converted_time.time()

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
        try:
            feedback = {
                "id": self.id,
                "objectId": self.objectId,
                "comment": self.comment,
                "branch": self.branch.name,
                "city": self.branch.city.name,
                "region": self.branch.city.region.name,
                "user_name": self.customer_name(),
                "user_phone": self.customer_phone(),
                "segment": self.get_segment(),
                "shift": self.get_shift(),
                "is_negative": self.is_negative(),
                "action_taken": self.action_taken,
                "email": self.customer_email(),
                "created_at": self.created_at,
            }
            return feedback
        except Exception as e:
            return {}


class FeedbackOptionQuerySet(models.QuerySet):
    def question(self, question_type):
        question = Question.objects.get(type=question_type)
        return self.filter(option__in=question.options.values_list('id'))

    def date(self, date_from, date_to):
        if date_to and date_from:
            current_tz = timezone.get_current_timezone()
            date_to = current_tz.localize(datetime.strptime(date_to + " 23:59:59", constants.DATE_FORMAT))
            date_from = current_tz.localize(datetime.strptime(date_from + " 00:00:00", constants.DATE_FORMAT))
            return self.filter(created_at__gt=date_from, created_at__lte=date_to)
        return self

    def filters(self, region_id, city_id, branch_id, area_id=None):
        if region_id and city_id and branch_id:
            return self.filter(
                feedback__branch__exact=branch_id,
                feedback__branch__city__exact=city_id,
                feedback__branch__city__region__exact=region_id)
        elif region_id and city_id:
            return self.filter(
                feedback__branch__city__exact=city_id,
                feedback__branch__city__region__exact=region_id)
        elif region_id:
            return self.filter(feedback__branch__city__region__exact=region_id)
        elif branch_id:
            return self.filter(feedback__branch__exact=branch_id)
        elif area_id:
            return self.filter(feedback__branch__city__region__area__exact=area_id)
        return self

    def related_filters(self, type, object):
        if type == constants.CITY_ANALYSIS:
            return self.filter(feedback__branch__city__exact=object.id)
        elif type == constants.BRANCH_ANALYSIS:
            return self.filter(feedback__branch__exact=object.id)
        elif type == constants.REGIONAL_ANALYSIS:
            return self.filter(feedback__branch__city__region__exact=object.id)
        else:
            return self.filter(feedback__branch__city__region__area__exact=object.id)

    def feedback(self, option):
        return self.filter(feedback__in=FeedbackOption.objects.filter(option=option).values_list('feedback_id'))

    def children(self, option):
        return self.filter(option__in=option.children.values_list('id'))

    def question_children(self, question, option):
        return self.filter(option__in=question.options.filter(parent=option.id).values_list('id'))

    def question_parent_options(self, question):
        return self.filter(option__in=question.options.filter(parent=None).values_list('id'))

    def options(self, options):
        return self.filter(option__in=options.values_list('id'))

    def promotion_options(self, question):
        return self.filter(option__in=question.options.filter().values_list('id'))


class FeedbackOptionManager(models.Manager):
    def get_query_set(self):
        return FeedbackOptionQuerySet(FeedbackOption)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


class FeedbackOption(models.Model):
    feedback = models.ForeignKey(Feedback, related_name='feedback_option')
    option = models.ForeignKey(Option, related_name='feedback_option')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = models.Manager()
    manager = FeedbackOptionManager()

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

    @staticmethod
    def get_if_exists(objectId):
        feedback_option = FeedbackOption.objects.filter(objectId=objectId).first()
        if feedback_option:
            return feedback_option

    @staticmethod
    def get_if_exists(feedback_id, option_id):
        feedback_option = FeedbackOption.objects.filter(feedback_id=feedback_id, option_id=option_id).first()
        if feedback_option:
            return feedback_option

    @staticmethod
    def get_top_option(date_from=None, date_to=None):
        result = None
        dict = FeedbackOption.manager.question(constants.TYPE_1).date(date_from, date_to).values('option_id').annotate(count=Count("option_id"))
        if dict:
            dict = dict.latest("count")
            option = Option.objects.get(pk=dict["option_id"])
            result = {"count": dict["count"], "option_text": option.text, "option_id": option.id}
        return result

    @staticmethod
    def get_qsc_count(date_from=None, date_to=None):
        dict_list = FeedbackOption.manager.question(constants.TYPE_2).date(date_from, date_to).values('option_id').annotate(count=Count("option_id"))

        qsc_list = []
        for dict in dict_list:
            option = Option.objects.get(pk=dict["option_id"])
            qsc_list.append({"count": dict["count"], "option_text": option.text, "option_id": option.id})

        return qsc_list


class Concern(models.Model):
    keyword = models.CharField(max_length=255, db_index=True, unique=True)
    count = models.IntegerField(db_index=True, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def to_dict(self):
        try:
            concern = {
                "id": self.id,
                "name": self.keyword.capitalize(),
                "weight": self.count,
            }
            return concern
        except Exception as e:
            return {}

    @staticmethod
    def get_if_exists(keyword):
        concern = Concern.objects.filter(keyword=keyword).first()
        if concern:
            return concern

    @staticmethod
    def get_all_concerns():
        return Concern.objects.filter(is_active=True)