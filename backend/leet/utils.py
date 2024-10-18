import datetime
import functools
import operator
import os

from django.conf import settings
from django.db import models as orm
from django.utils import timezone

from leet import constants
from leet import models


def get_from_nested_structure(
        structure, map_list, default=None, func=operator.getitem):
    """
    Get deep value from nested structures - dict, object
    https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
    """
    if not structure:
        return default
    try:
        return functools.reduce(func, map_list, structure)
    except (TypeError, KeyError, AttributeError):
        return default


def get_photo_path(instance, filename):  # pylint: disable=unused-argument
    """
    Get the upload image file path.
    :param filename: File name
    :return: Upload file path
    """
    image_path = os.path.join(settings.MEDIA_ROOT,
                              settings.USER_PHOTO_DIR, filename)

    return image_path


def get_candidate_statuses_dict():
    return dict(
        ((s.upper(), s) for s in
         models.CandidateStatus.objects.values_list('name', flat=True)))


def get_dynamic_queries(values_list, operator_=operator.and_):
    """
    Return django orm.Q queries for filters with operators.
    :param values_list:    list of dicts.
    :param operator_:      operator or_ or and_ for logical '|' or '&'
                           default value and_
    :return: clauses for filters, for example:
                orm.Q(first_clauses)
                |
                orm.Q(second_claueses)
    """
    return functools.reduce(operator_, (orm.Q(**i) for i in values_list))


def ago(number_days):
    return timezone.now().date() - datetime.timedelta(days=number_days)


def get_user_online_status(user):
    if hasattr(user, 'activity'):
        time_delta = datetime.timedelta(
            minutes=settings.USER_CONSIDERED_ONLINE_TIME_DELTA)
        return timezone.now() - user.activity.last_activity < time_delta
    return False


def cents_to_dollars(cents):
    return cents / constants.CENTS_IN_DOLLAR


def timestamp_to_utc_datetime(timestamp):
    return datetime.datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc
    )
