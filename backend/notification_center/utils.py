import collections
import operator

from django.contrib import auth

from leet import enums
from leet import utils
from notification_center import constants
from notification_center import models


USER_MODEL = auth.get_user_model()


def get_grouped_notification_types(queryset):
    result = collections.OrderedDict([
        (constants.NOTIFICATION_FORMAT_WEB, []),
        (constants.NOTIFICATION_FORMAT_EMAIL, [])
    ])
    for i in queryset:
        result[i.format].append({
            'id': i.id,
            'name': i.name
        })
    return result


def get_web_notifications():
    return (models.NotificationType
            .objects
            .filter(format=constants.NOTIFICATION_FORMAT_WEB))


def get_email_notifications():
    return (models.NotificationType
            .objects
            .filter(format=constants.NOTIFICATION_FORMAT_EMAIL))


def get_autoapply_web_notif_type():
    return get_web_notifications().get(
        name=constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS
    )


def get_autoapply_email_notif_type():
    return get_email_notifications().get(
        name=constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS
    )


def get_invitation_received_email_notif_type():
    return get_email_notifications().get(
        name=constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
    )


def get_subscribed_notif_verbs(user):
    sub_notif_ids = user.subscribed_notifications.values_list('id', flat=True)
    verbs = (models.NotificationVerb
                   .objects
                   .filter(type__id__in=sub_notif_ids)
                   .values_list('name', flat=True))
    return verbs


def get_subscribed_users(notif):
    return set(USER_MODEL
               .objects
               .filter(subscribed_notifications__id=notif.id)
               .values_list('id', flat=True))


def get_notif_types_for_manage(user, queryset):
    groups_names = user.groups.values_list('name', flat=True)
    if enums.AuthGroupsEnum.COMPANY_USER.value in groups_names:  # noqa
        return queryset.none()
    values_list = constants.NOTIFICATION_TYPES_CAN_DISABLE_JOB_SEEKER
    queries = utils.get_dynamic_queries(values_list, operator_=operator.or_)
    return queryset.filter(queries)
